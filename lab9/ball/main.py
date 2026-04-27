import pygame
from ball import Ball

pygame.init()

WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball Game")

clock = pygame.time.Clock()

ball = Ball(WIDTH // 2, HEIGHT // 2, 50, BLUE, WIDTH, HEIGHT)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.move_up()
            elif event.key == pygame.K_DOWN:
                ball.move_down()
            elif event.key == pygame.K_LEFT:
                ball.move_left()
            elif event.key == pygame.K_RIGHT:
                ball.move_right()

    screen.fill(WHITE)
    ball.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()