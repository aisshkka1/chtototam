import pygame, sys, random, time
from racer import *
from ui import Button, TextInput
from persistence import save_score, load_leaderboard, save_settings, load_settings

# --- Настройки экрана и инициализация ---
pygame.init()
SURFACE = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Racer Game")
background = pygame.image.load("AnimatedStreet.png")
clock = pygame.time.Clock()
FPS = 60
username = "Player"

def leaderboard_screen():
    scores = load_leaderboard() 
    btn_back = Button(125, 530, 150, 40, "Back")
    
    while True:
        SURFACE.fill((30, 30, 30))
        font = pygame.font.SysFont("Verdana", 20)
        title = pygame.font.SysFont("Verdana", 35).render("TOP 10 RACERS", True, (255, 215, 0))
        SURFACE.blit(title, (60, 30))

        for i, entry in enumerate(scores):
            txt = f"{i+1}. {entry['name'][:10]} | {entry['score']} pts"
            img = font.render(txt, True, (255, 255, 255))
            SURFACE.blit(img, (50, 100 + i * 35))

        btn_back.draw(SURFACE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and btn_back.is_clicked(event.pos):
                return

        pygame.display.update()

def name_entry_screen():
    global username
    input_box = TextInput(100, 250, 200, 40)
    btn_start = Button(125, 350, 150, 50, "Start Game", (0, 200, 0))
    
    while True:
        SURFACE.fill((50, 50, 50))
        txt = pygame.font.SysFont("Verdana", 25).render("Enter Your Name:", True, (255, 255, 255))
        SURFACE.blit(txt, (100, 200))
        
        input_box.draw(SURFACE)
        btn_start.draw(SURFACE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            input_box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and btn_start.is_clicked(event.pos):
                if input_box.text.strip():
                    username = input_box.text
                    play_game()
                    return
        pygame.display.update()

def play_game():
    # 1. Логика выбора картинки машины (Пункт 3.5)
    car_files = {
        "red": "Enemy.png",
        "blue": "Player.png",
        "green": "Sprite_green_car-2.png"
    }
    
    chosen_color = current_settings.get("car_color", "blue")
    image_to_load = car_files.get(chosen_color, "Player.png")
    
    # 2. Инициализация игрока и групп спрайтов
    player = Player(image_to_load)
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    
    # 3. Игровые показатели
    items_collected = 0
    active_powerup = None
    powerup_timer = 0
    distance = 0
    finish_line = 3000 
    
    # 4. Применение сложности из настроек (Пункт 3.5)
    diff_speeds = {"Easy": 3, "Medium": 5, "Hard": 8}
    base_speed = diff_speeds.get(current_settings.get("difficulty", "Medium"), 5)

    is_slowed = False
    running = True

    while running:
        current_time = pygame.time.get_ticks()

        if active_powerup and current_time > powerup_timer:
            active_powerup = None

        spawn_rate = max(20, 60 - int(distance // 500)) 
        temp_speed = base_speed * 2 if active_powerup == "nitro" else base_speed
        current_speed = temp_speed / 2 if is_slowed else temp_speed
        
        distance += current_speed / 10
        
        # Проверка финиша
        if distance >= finish_line:
            save_score(username, items_collected, distance)
            game_over_screen(items_collected, int(distance), win=True)
            return

        SURFACE.blit(background, (0,0))
        
        # Спавн
        if len(enemies) < 3 and random.randint(1, spawn_rate) == 1:
            enemies.add(Enemy(player.rect.centerx))
        if random.randint(1, 150) == 1:
            obstacles.add(Obstacle(random.choice(['oil', 'barrier'])))
        if random.randint(1, 100) == 1:
            coins.add(Coin())
        if random.randint(1, 150) == 1: # Частый спавн бонусов
            powerups.add(PowerUp(random.choice(['nitro', 'shield', 'repair'])))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        player.move()
        enemies.update(current_speed)
        coins.update(current_speed)
        obstacles.update(current_speed)
        powerups.update(current_speed)

        # Коллизии Препятствия
        obs_hit = pygame.sprite.spritecollideany(player, obstacles)
        if obs_hit:
            if obs_hit.type == 'oil': 
                is_slowed = True
            else:
                if active_powerup == "shield":
                    active_powerup = None
                    obs_hit.kill()
                else:
                    save_score(username, items_collected, int(distance))
                    game_over_screen(items_collected, int(distance))
                    return
        else:
            is_slowed = False

        # Сбор монет
        coin_hit = pygame.sprite.spritecollideany(player, coins)
        if coin_hit:
            items_collected += coin_hit.weight 
            coin_hit.kill()

        # Сбор бонусов
        p_hit = pygame.sprite.spritecollideany(player, powerups)
        if p_hit:
            items_collected += 1 
            if p_hit.kind == 'repair':
                for o in obstacles: o.kill()
            else:
                active_powerup = p_hit.kind
                powerup_timer = current_time + 5000 
            p_hit.kill()
        
        # Враги
        if pygame.sprite.spritecollideany(player, enemies):
            if active_powerup == "shield":
                active_powerup = None
                for e in enemies: e.kill()
            else:
                save_score(username, items_collected, int(distance))
                game_over_screen(items_collected, int(distance))
                return

        # Отрисовка
        SURFACE.blit(player.image, player.rect)
        enemies.draw(SURFACE)
        coins.draw(SURFACE)
        obstacles.draw(SURFACE)
        powerups.draw(SURFACE)
        
        # UI
        font = pygame.font.SysFont("Verdana", 20)
        remaining = max(0, int(finish_line - distance))
        SURFACE.blit(font.render(f"Score: {items_collected}", True, (0,0,0)), (10, 10))
        SURFACE.blit(font.render(f"To Finish: {remaining}m", True, (0,0,0)), (10, 35))
        
        if active_powerup:
            time_left = max(0, (powerup_timer - current_time) // 1000)
            p_txt = font.render(f"ACTIVE: {active_powerup.upper()} ({time_left}s)", True, (255, 0, 0))
            SURFACE.blit(p_txt, (10, 60))
        
        pygame.display.update()
        clock.tick(FPS)


current_settings = load_settings()

def settings_screen():
    global current_settings
    
    # Кнопки настроек
    btn_sound = Button(100, 150, 200, 50, f"Sound: {'ON' if current_settings['sound'] else 'OFF'}")
    btn_color = Button(100, 220, 200, 50, f"Color: {current_settings['car_color'].upper()}")
    btn_diff = Button(100, 290, 200, 50, f"Diff: {current_settings['difficulty']}")
    btn_back = Button(125, 450, 150, 40, "Save & Back", (0, 200, 0))
        

    colors = ["red", "blue", "green"]
    difficulties = ["Easy", "Medium", "Hard"]

    while True:
        SURFACE.fill((50, 50, 50))
        title = pygame.font.SysFont("Verdana", 30).render("SETTINGS", True, (255, 255, 255))
        SURFACE.blit(title, (120, 50))

        btn_sound.draw(SURFACE)
        btn_color.draw(SURFACE)
        btn_diff.draw(SURFACE)
        btn_back.draw(SURFACE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Переключатель звука
                if btn_sound.is_clicked(event.pos):
                    current_settings["sound"] = not current_settings["sound"]
                    btn_sound.text = f"Sound: {'ON' if current_settings['sound'] else 'OFF'}"
                
                # Переключатель цвета
                if btn_color.is_clicked(event.pos):
                    idx = (colors.index(current_settings["car_color"]) + 1) % len(colors)
                    current_settings["car_color"] = colors[idx]
                    btn_color.text = f"Color: {current_settings['car_color'].upper()}"
                
                # Переключатель сложности
                if btn_diff.is_clicked(event.pos):
                    idx = (difficulties.index(current_settings["difficulty"]) + 1) % len(difficulties)
                    current_settings["difficulty"] = difficulties[idx]
                    btn_diff.text = f"Diff: {current_settings['difficulty']}"

                if btn_back.is_clicked(event.pos):
                    save_settings(current_settings) # Сохраняем в JSON
                    return

        pygame.display.update()

def main_menu():
    while True:
        SURFACE.fill((34, 139, 34)) 
        btn_play = Button(125, 120, 150, 50, "Play")
        btn_leads = Button(125, 200, 150, 50, "Leaderboard") # Y было слишком маленьким
        btn_settings = Button(125, 280, 150, 50, "Settings")    # Добавили пространство
        btn_quit = Button(125, 360, 150, 50, "Quit")

        btn_play.draw(SURFACE)
        btn_leads.draw(SURFACE)
        btn_settings.draw(SURFACE)
        btn_quit.draw(SURFACE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_play.is_clicked(event.pos): name_entry_screen()
                if btn_leads.is_clicked(event.pos): leaderboard_screen()
                if btn_settings.is_clicked(event.pos): settings_screen() 
                if btn_quit.is_clicked(event.pos): pygame.quit(); sys.exit()
        
        pygame.display.update()

def game_over_screen(score, dist, win=False):
    btn_retry = Button(125, 350, 150, 50, "Retry", (100, 255, 100))
    btn_menu = Button(125, 420, 150, 50, "Main Menu", (200, 200, 200))

    while True:
        SURFACE.fill((200, 0, 0) if not win else (0, 150, 0))
        msg = "YOU WIN!" if win else "GAME OVER"
        
        font = pygame.font.SysFont("Verdana", 40)
        SURFACE.blit(font.render(msg, True, (255, 255, 255)), (80, 100))
        
        # Показываем финальную статистику
        info_font = pygame.font.SysFont("Verdana", 20)
        SURFACE.blit(info_font.render(f"Final Score: {score}", True, (255, 255, 255)), (110, 200))
        SURFACE.blit(info_font.render(f"Distance: {int(dist)}m", True, (255, 255, 255)), (110, 240))

        btn_retry.draw(SURFACE)
        btn_menu.draw(SURFACE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_retry.is_clicked(event.pos): play_game(); return
                if btn_menu.is_clicked(event.pos): return # Выход в main_menu

        pygame.display.update()

if __name__ == "__main__":
    main_menu()