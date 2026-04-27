import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# --- Colors ---
colorWHITE = (255, 255, 255)
colorGRAY = (200, 200, 200)
colorBLACK = (0, 0, 0)
colorRED = (255, 0, 0)
colorGREEN = (0, 255, 0)
colorBLUE = (0, 0, 255)
colorYELLOW = (255, 255, 0)

# Constants
WIDTH = 600
HEIGHT = 600
CELL = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake: Weighted & Timed Food")

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
        head = self.body[0]
        if head.x >= WIDTH // CELL or head.x < 0 or head.y >= HEIGHT // CELL or head.y < 0:
            return True
        return False

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

# --- Task: Food with Weights and Timer ---
class Food:
    def __init__(self, snake_body):
        self.pos = Point(0, 0)
        self.weight = 1
        self.timer = 0
        self.max_time = 40 # Food lasts 40 frames (~8 seconds at 5 FPS)
        self.generate_random_pos(snake_body)

    def draw(self):
        # Draw different weights with different sizes/colors
        # Weight 3 is Blue, Weight 2 is Green, Weight 1 is small Green
        color = colorGREEN
        size_offset = 0
        
        if self.weight == 3:
            color = colorBLUE
        elif self.weight == 2:
            size_offset = 2 # Slightly larger

        pygame.draw.rect(screen, color, (self.pos.x * CELL + size_offset, 
                                         self.pos.y * CELL + size_offset, 
                                         CELL - size_offset*2, CELL - size_offset*2))

    def generate_random_pos(self, snake_body):
        # Task: Randomly generating food with different weights
        self.weight = random.choices([1, 2, 3], weights=[70, 20, 10])[0]
        self.timer = 0 # Reset timer for new food
        
        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1)
            self.pos.y = random.randint(0, HEIGHT // CELL - 1)
            on_snake = any(s.x == self.pos.x and s.y == self.pos.y for s in snake_body)
            if not on_snake:
                break

    def update(self, snake_body):
        # Task: Foods which are disappearing after some time
        self.timer += 1
        if self.timer >= self.max_time:
            self.generate_random_pos(snake_body)

# Game state
snake = Snake()
food = Food(snake.body)
score = 0
level = 1
FPS = 5
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
    food.update(snake.body) # Update the timer for the food

    if snake.check_border():
        screen.fill(colorRED)
        msg = font_big.render("GAME OVER", True, colorWHITE)
        screen.blit(msg, (WIDTH//2 - 180, HEIGHT//2 - 30))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    # Collision with Food
    head = snake.body[0]
    if head.x == food.pos.x and head.y == food.pos.y:
        # Task: Snake grows and score increases based on weight
        score += food.weight
        for _ in range(food.weight):
            snake.body.append(Point(-1, -1))
        
        # Level up logic
        if score // 5 >= level:
            level += 1
            FPS += 2 
            
        food.generate_random_pos(snake.body)

    # Drawing
    draw_grid_chess()
    snake.draw()
    food.draw()

    # UI
    score_txt = font_small.render(f"Score: {score}", True, colorBLACK)
    level_txt = font_small.render(f"Level: {level}", True, colorBLACK)
    # Visual Timer bar
    timer_width = (food.max_time - food.timer) * (CELL // 2) / 10
    pygame.draw.rect(screen, colorRED, (10, 40, timer_width, 5))

    screen.blit(score_txt, (10, 10))
    screen.blit(level_txt, (WIDTH - 110, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()