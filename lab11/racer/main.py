import pygame, sys
from pygame.locals import *
import random, time

# Initializing Pygame
pygame.init()

# Load and play background music immediately
# -1 means the music will loop infinitely
pygame.mixer.Sound('background.wav').play(-1)

# Setting up FPS (Frames Per Second) to keep game speed consistent
FPS = 60
FramePerSec = pygame.time.Clock()

# Defining Color constants
BLUE   = (0, 0, 255)
RED    = (255, 0, 0)
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
YELLOW = (255, 255, 0)
GOLD   = (255, 215, 0) # Color for heavier coins

# Game Variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5        # Initial speed of the game
SCORE = 0        # Number of enemies passed
COIN_SCORE = 0   # Total value/weight of coins collected
N_COINS = 5      # Task: Increase speed every time player earns this many coins

# Setting up Fonts for text rendering
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load the road background image
background = pygame.image.load("AnimatedStreet.png")

# Create the display window
DISPLAYSURF = pygame.display.set_mode((400,600))
pygame.display.set_caption("Racer: Extended Version")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        # Spawn enemy at a random horizontal position at the top
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0) 

    def move(self):
        global SCORE
        # Move enemy downward based on current global SPEED
        self.rect.move_ip(0, SPEED)
        # If enemy goes off screen, reset to top and increase score
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Task: Class for coins with different weights
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = 1 # Default weight
        self.spawn()

    def spawn(self):
        # Task: Randomly generating food/coins with different weights
        # 80% chance for weight 1 (Yellow), 20% chance for weight 3 (Gold)
        self.weight = random.choices([1, 3], weights=[80, 20])[0]
        
        # Create coin image based on weight
        size = 20 if self.weight == 1 else 30
        color = YELLOW if self.weight == 1 else GOLD
        
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2)
        
        self.rect = self.image.get_rect()
        # Position at random X, and slightly above top of screen
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)

    def move(self):
        # Coins fall at the same speed as the road
        self.rect.move_ip(0, SPEED)
        # If coin missed, respawn at top
        if (self.rect.top > 600):
            self.spawn()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        # Handle left/right movement with arrow keys
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

# Setup Sprite instances
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Organize sprites into groups for easier management
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw the road background
    DISPLAYSURF.blit(background, (0,0))
    
    # Render and display Scores
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    coin_text = font_small.render("Coins: " + str(COIN_SCORE), True, BLACK)
    
    DISPLAYSURF.blit(scores, (10,10))
    # Requirement: Show coins in top right corner
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 120, 10))

    # Update positions and draw all sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Task: Collision detection for Coins
    coin_hit = pygame.sprite.spritecollideany(P1, coins)
    if coin_hit:
        # Increase score by the weight of the coin (1 or 3)
        COIN_SCORE += coin_hit.weight
        
        # Task: Increase speed of Enemy when player earns N coins
        # Every time COIN_SCORE hits a multiple of N_COINS (e.g. 5, 10, 15...)
        if COIN_SCORE % N_COINS == 0:
            SPEED += 3 # Increase difficulty
            
        coin_hit.spawn() # Remove collected coin and spawn new one

    # Collision detection with Enemy (Game Over)
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('crash.wav').play()
          time.sleep(0.5)
          
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
          pygame.display.update()
          
          # Clean up
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()

    # Update the full display surface to the screen
    pygame.display.update()
    # Pause the loop to maintain 60 FPS
    FramePerSec.tick(FPS)