import pygame

# Initialize Pygame
pygame.init()

def main():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Paint")
    clock = pygame.time.Clock()
    
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    
    # Tool settings
    radius = 9
    drawing = False
    mode = 'brush'  # modes: brush, rectangle, circle, eraser
    color = BLUE
    
    # We use a second surface to keep our drawings permanent
    canvas = pygame.Surface((800, 600))
    canvas.fill(WHITE)

    # Variables to store starting positions for shapes
    start_pos = None

    while True:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                # Key shortcuts for colors
                if event.key == pygame.K_r: color = RED
                if event.key == pygame.K_g: color = GREEN
                if event.key == pygame.K_b: color = BLUE
                
                # Key shortcuts for tools
                if event.key == pygame.K_1: mode = 'brush'
                if event.key == pygame.K_2: mode = 'rectangle'
                if event.key == pygame.K_3: mode = 'circle'
                if event.key == pygame.K_4: mode = 'eraser'
                
                # Clear Canvas
                if event.key == pygame.K_c: canvas.fill(WHITE)

            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos # Mark where the mouse clicked
                
            if event.type == pygame.MOUSEBUTTONUP:
                # When mouse is released, draw the final shape onto the canvas
                if mode == 'rectangle':
                    draw_rect(canvas, color, start_pos, event.pos, radius)
                elif mode == 'circle':
                    draw_circle(canvas, color, start_pos, event.pos, radius)
                drawing = False

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if mode == 'brush':
                        # Draw directly to canvas for brush
                        pygame.draw.circle(canvas, color, event.pos, radius)
                    elif mode == 'eraser':
                        # Eraser is just a white brush
                        pygame.draw.circle(canvas, WHITE, event.pos, radius)

        # Draw the canvas first
        screen.blit(canvas, (0, 0))

        # Visual Feedback: Show the shape while dragging
        if drawing and mode == 'rectangle':
            draw_rect(screen, color, start_pos, pygame.mouse.get_pos(), radius)
        elif drawing and mode == 'circle':
            draw_circle(screen, color, start_pos, pygame.mouse.get_pos(), radius)

        # Draw a small UI Legend
        draw_ui(screen, mode, color)

        pygame.display.flip()
        clock.tick(60)

def draw_rect(surf, color, start, end, width):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(start[0] - end[0])
    h = abs(start[1] - end[1])
    if w > 0 and h > 0:
        pygame.draw.rect(surf, color, (x, y, w, h), width)

def draw_circle(surf, color, start, end, width):
    # Calculate distance between start and current mouse for radius
    rad = int(((start[0] - end[0])**2 + (start[1] - end[1])**2)**0.5)
    if rad > 0:
        pygame.draw.circle(surf, color, start, rad, width)

def draw_ui(screen, mode, color):
    font = pygame.font.SysFont("Arial", 18)
    txt = f"Mode: {mode.upper()} | Color: {color} | Keys: 1-Brush, 2-Rect, 3-Circle, 4-Eraser, C-Clear"
    text_surf = font.render(txt, True, (50, 50, 50))
    screen.blit(text_surf, (10, 10))

main()