import pygame
import math

def flood_fill(surface, pos, new_color):
    """Алгоритм заливки (Flood Fill) через очередь (BFS)."""
    target_color = surface.get_at(pos)
    if target_color == new_color: return
    
    width, height = surface.get_size()
    queue = [pos]
    surface.set_at(pos, new_color)
    
    idx = 0
    while idx < len(queue):
        curr_x, curr_y = queue[idx]
        idx += 1
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = curr_x + dx, curr_y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if surface.get_at((nx, ny)) == target_color:
                    surface.set_at((nx, ny), new_color)
                    queue.append((nx, ny))

def draw_shape(surf, mode, color, start, end, width):
    """Отрисовка всех фигур с учетом толщины (width)."""
    dx, dy = end[0] - start[0], end[1] - start[1]
    
    if mode == 'line':
        pygame.draw.line(surf, color, start, end, width)
    elif mode == 'rectangle':
        rect = pygame.Rect(min(start[0], end[0]), min(start[1], end[1]), abs(dx), abs(dy))
        pygame.draw.rect(surf, color, rect, width)
    elif mode == 'circle':
        radius = int(math.hypot(dx, dy))
        pygame.draw.circle(surf, color, start, radius, width)
    elif mode == 'square':
        side = max(abs(dx), abs(dy))
        rect = pygame.Rect(start[0] if dx > 0 else start[0]-side, start[1] if dy > 0 else start[1]-side, side, side)
        pygame.draw.rect(surf, color, rect, width)
    elif mode == 'right_triangle':
        pygame.draw.polygon(surf, color, [start, end, (start[0], end[1])], width)
    elif mode == 'equilateral_triangle':
        side = abs(dx)
        h = int(side * math.sqrt(3) / 2)
        p1 = (start[0], start[1] - h if dy < 0 else start[1])
        p2 = (p1[0] - side//2, p1[1] + (h if dy > 0 else -h))
        p3 = (p1[0] + side//2, p1[1] + (h if dy > 0 else -h))
        pygame.draw.polygon(surf, color, [p1, p2, p3], width)
    elif mode == 'rhombus':
        mid_x, mid_y = start[0] + dx // 2, start[1] + dy // 2
        points = [(mid_x, start[1]), (end[0], mid_y), (mid_x, end[1]), (start[0], mid_y)]
        pygame.draw.polygon(surf, color, points, width)