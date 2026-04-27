import pygame
import os
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("Arial", 28)
clock = pygame.time.Clock()

music_folder = os.path.join(os.path.dirname(__file__), "music")
player = MusicPlayer(music_folder)

running = True

print("Controls: P=Play, S=Stop, N=Next, B=Back, Q=Quit")

while running:
    screen.fill((255, 255, 255))

    # 🎹 EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()

            elif event.key == pygame.K_s:
                player.stop()

            elif event.key == pygame.K_n:
                player.next()

            elif event.key == pygame.K_b:
                player.previous()

            elif event.key == pygame.K_q:
                running = False

    # 🎵 UI DISPLAY
    track = player.get_current_track()

    if track:
        # 🎧 Track name
        name = os.path.basename(track)
        text = font.render("Now Playing:", True, (0, 0, 0))
        screen.blit(text, (50, 100))

        name_text = font.render(name, True, (0, 0, 255))
        screen.blit(name_text, (50, 140))

        # 📊 PLAYLIST POSITION
        pos_text = font.render(
            f"{player.current_index + 1} / {len(player.playlist)}",
            True,
            (100, 100, 100)
        )
        screen.blit(pos_text, (50, 180))

        # ⏱️ REAL TIME PROGRESS (FIXED)
        current_time = player.get_position()
        time_text = font.render(f"Time: {current_time}s", True, (0, 150, 0))
        screen.blit(time_text, (50, 220))

    else:
        text = font.render("No music found", True, (255, 0, 0))
        screen.blit(text, (50, 150))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()