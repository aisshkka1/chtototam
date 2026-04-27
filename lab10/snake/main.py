import pygame
import random
import sys
# Assuming color_palette.py is in the same folder
from color_palette import * 
pygame.init()

# Constants
WIDTH = 600
HEIGHT = 600
CELL = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Leveler")

# Fonts
font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 60)

def draw_grid_chess():
    colors = [colorWHITE, colorGRAY]
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colors[(i + j) % 2], (j * CELL, i * CELL, CELL, CELL))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def check_border(self):
        # Task: Checking for border (wall) collision
        head = self.body[0]
        if head.x >= WIDTH // CELL or head.x < 0 or head.y >= HEIGHT // CELL or head.y < 0:
            return True
        return False

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

class Food:
    def __init__(self, snake_body):
        self.pos = Point(0, 0)
        self.generate_random_pos(snake_body)

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self, snake_body):
        # Task: Generate random position so it does not fall on the snake
        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1)
            self.pos.y = random.randint(0, HEIGHT // CELL - 1)
            
            # Check if this point is inside the snake
            on_snake = False
            for segment in snake_body:
                if segment.x == self.pos.x and segment.y == self.pos.y:
                    on_snake = True
                    break
            
            if not on_snake:
                break

# Game state variables
snake = Snake()
food = Food(snake.body)
score = 0
level = 1
FPS = 5 # Initial speed
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx, snake.dy = 1, 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx, snake.dy = -1, 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx, snake.dy = 0, 1
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx, snake.dy = 0, -1

    snake.move()

    # Collision with Border
    if snake.check_border():
        screen.fill(colorRED)
        msg = font_big.render("CRASHED!", True, colorWHITE)
        screen.blit(msg, (WIDTH//2 - 140, HEIGHT//2 - 30))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    # Collision with Food
    head = snake.body[0]
    if head.x == food.pos.x and head.y == food.pos.y:
        score += 1
        snake.body.append(Point(head.x, head.y))
        food.generate_random_pos(snake.body)
        
        # Task: Add levels (Every 3 foods) and increase speed
        if score % 3 == 0:
            level += 1
            FPS += 2 # Increase speed

    # Draw everything
    draw_grid_chess()
    snake.draw()
    food.draw()

    # Task: Add counter to score and level
    score_txt = font_small.render(f"Score: {score}", True, colorBLACK)
    level_txt = font_small.render(f"Level: {level}", True, colorBLACK)
    screen.blit(score_txt, (10, 10))
    screen.blit(level_txt, (WIDTH - 100, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()