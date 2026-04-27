import pygame
import math

# Initialize Pygame
pygame.init()

def main():
    screen = pygame.display.set_mode((900, 700))
    pygame.display.set_caption("Extended Paint: Geometric Shapes")
    clock = pygame.time.Clock()
    
    # Colors
    WHITE, BLACK = (255, 255, 255), (0, 0, 0)
    RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
    
    # Settings
    radius = 2 # Border thickness for shapes
    drawing = False
    mode = 'brush' # Current tool
    color = BLACK
    
    # Canvas setup
    canvas = pygame.Surface((900, 700))
    canvas.fill(WHITE)
    start_pos = None

    while True:
        curr_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                # Tool Selection Keys
                if event.key == pygame.K_1: mode = 'brush'
                if event.key == pygame.K_2: mode = 'square'
                if event.key == pygame.K_3: mode = 'right_triangle'
                if event.key == pygame.K_4: mode = 'equilateral_triangle'
                if event.key == pygame.K_5: mode = 'rhombus'
                if event.key == pygame.K_e: mode = 'eraser'
                if event.key == pygame.K_c: canvas.fill(WHITE)

            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos
                
            if event.type == pygame.MOUSEBUTTONUP:
                # Task: Finalize drawing on the permanent canvas
                if mode != 'brush' and mode != 'eraser':
                    draw_shape(canvas, mode, color, start_pos, event.pos, radius)
                drawing = False

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if mode == 'brush':
                        pygame.draw.circle(canvas, color, event.pos, radius + 5)
                    elif mode == 'eraser':
                        pygame.draw.circle(canvas, WHITE, event.pos, 20)

        # Draw the saved canvas
        screen.blit(canvas, (0, 0))

        # Task: Show "Ghost" shape while dragging for better UX
        if drawing and mode not in ['brush', 'eraser']:
            draw_shape(screen, mode, color, start_pos, curr_pos, radius)

        # UI Overlay
        draw_ui(screen, mode)

        pygame.display.flip()
        clock.tick(60)

# --- Geometric Drawing Functions ---

def draw_shape(surf, mode, color, start, end, width):
    dx = end[0] - start[0]
    dy = end[1] - start[1]

    if mode == 'square':
        # Square: All sides equal, so we take the larger of dx/dy
        side = max(abs(dx), abs(dy))
        rect_x = start[0] if dx > 0 else start[0] - side
        rect_y = start[1] if dy > 0 else start[1] - side
        pygame.draw.rect(surf, color, (rect_x, rect_y, side, side), width)

    elif mode == 'right_triangle':
        # Right Triangle: Uses start, end, and a point that shares x of end and y of start
        points = [start, end, (start[0], end[1])]
        pygame.draw.polygon(surf, color, points, width)

    elif mode == 'equilateral_triangle':
        # Equilateral Triangle: Sides equal, calculated using height = side * sqrt(3)/2
        side = abs(dx)
        height = int(side * math.sqrt(3) / 2)
        # Point 1: Top, Point 2: Bottom Left, Point 3: Bottom Right
        p1 = (start[0], start[1] - height if dy < 0 else start[1])
        p2 = (p1[0] - side//2, p1[1] + height if dy > 0 else p1[1] - height)
        p3 = (p1[0] + side//2, p1[1] + height if dy > 0 else p1[1] - height)
        pygame.draw.polygon(surf, color, [p1, p2, p3], width)

    elif mode == 'rhombus':
        # Rhombus: Diamond shape based on the bounding box of mouse drag
        mid_x = start[0] + dx // 2
        mid_y = start[1] + dy // 2
        points = [
            (mid_x, start[1]), # Top
            (end[0], mid_y),   # Right
            (mid_x, end[1]),   # Bottom
            (start[0], mid_y)  # Left
        ]
        pygame.draw.polygon(surf, color, points, width)

def draw_ui(screen, mode):
    font = pygame.font.SysFont("Verdana", 16)
    instructions = "1:Brush | 2:Square | 3:Right-Tri | 4:Equi-Tri | 5:Rhombus | E:Eraser | C:Clear"
    text = font.render(f"MODE: {mode.upper()}  |  {instructions}", True, (100, 100, 100))
    screen.blit(text, (15, 15))

main()