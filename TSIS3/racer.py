import pygame
import random
from pygame.locals import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__() 
        try:
            # 1. Загружаем картинку
            original_image = pygame.image.load(filename)
            
            # 2. Масштабируем её (ставим размер 40 пикселей в ширину и 80 в высоту)
            # Ты можешь поменять эти цифры, если хочешь сделать машину еще меньше
            self.image = pygame.transform.scale(original_image, (40, 80))
            
        except:
            # Запасной вариант, если файл не найден
            self.image = pygame.Surface((40, 80))
            self.image.fill((0, 255, 0))
            
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player_x):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        spawn_x = random.randint(40, SCREEN_WIDTH-40)
        while abs(spawn_x - player_x) < 80:
            spawn_x = random.randint(40, SCREEN_WIDTH-40)
        self.rect.center = (spawn_x, -100) 

    def update(self, speed):
        self.rect.move_ip(0, speed)
        if (self.rect.top > SCREEN_HEIGHT):
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        if type == 'oil':
            self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, (30, 30, 30, 150), (0,0,50,30))
        else:
            self.image = pygame.Surface((40, 20))
            self.image.fill((139, 69, 19)) 
        
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, SCREEN_WIDTH-50), -50)

    def update(self, speed):
        self.rect.y += speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = random.choice([1, 1, 1, 5]) 
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        color = (255, 215, 0) if self.weight == 5 else (255, 255, 0)
        pygame.draw.circle(self.image, color, (12, 12), 12)
        pygame.draw.circle(self.image, (0,0,0), (12, 12), 12, 1) # Обводка
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -50)

    def update(self, speed):
        self.rect.y += speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, kind):
        super().__init__()
        self.kind = kind
        colors = {'nitro': (255, 0, 255), 'shield': (0, 255, 255), 'repair': (0, 255, 0)}
        self.image = pygame.Surface((30, 30))
        self.image.fill(colors[kind])
        pygame.draw.rect(self.image, (255, 255, 255), (0,0,30,30), 2) # Рамка
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, SCREEN_WIDTH-50), -50)
        self.spawn_time = pygame.time.get_ticks()

    def update(self, speed):
        self.rect.y += speed
        if self.rect.top > SCREEN_HEIGHT or pygame.time.get_ticks() - self.spawn_time > 8000:
            self.kill()