import pygame
import datetime
from tools import draw_shape, flood_fill

pygame.init()

def main():
    # Настройка окна (с учетом места под меню)
    WIDTH, HEIGHT = 1000, 800
    MENU_H = 60
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS 2: Extended Paint Application")
    
    # Холст (отдельная поверхность)
    canvas = pygame.Surface((WIDTH, HEIGHT - MENU_H))
    canvas.fill((255, 255, 255))
    
    clock = pygame.time.Clock()
    mode, color, thickness = 'pencil', (0, 0, 0), 2
    drawing = False
    start_pos, last_pos = (0, 0), (0, 0)
    
    # Состояние текста
    text_active, text_content, text_pos = False, "", (0, 0)

    while True:
        m_pos = pygame.mouse.get_pos()
        # Корректируем координаты мыши относительно холста (вычитаем высоту меню)
        adj_pos = (m_pos[0], m_pos[1] - MENU_H)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return

            if event.type == pygame.KEYDOWN:
                if text_active:
                    if event.key == pygame.K_RETURN:
                        font = pygame.font.SysFont("Arial", 24)
                        canvas.blit(font.render(text_content, True, color), text_pos)
                        text_active = False
                    elif event.key == pygame.K_ESCAPE: text_active = False
                    elif event.key == pygame.K_BACKSPACE: text_content = text_content[:-1]
                    else: text_content += event.unicode
                else:
                    # Инструменты
                    keys = {pygame.K_p:'pencil', pygame.K_l:'line', pygame.K_r:'rectangle', 
                            pygame.K_c:'circle', pygame.K_s:'square', pygame.K_t:'right_triangle', 
                            pygame.K_u:'equilateral_triangle', pygame.K_d:'rhombus', 
                            pygame.K_f:'fill', pygame.K_x:'text', pygame.K_e:'eraser'}
                    if event.key in keys: mode = keys[event.key]
                    
                    # Размеры (3.2)
                    if event.key == pygame.K_1: thickness = 2
                    if event.key == pygame.K_2: thickness = 5
                    if event.key == pygame.K_3: thickness = 10
                    
                    # Очистка
                    if event.key == pygame.K_k: canvas.fill((255,255,255))

                    # Сохранение (3.4)
                    if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                        fn = f"paint_{datetime.datetime.now().strftime('%H%M%S')}.png"
                        pygame.image.save(canvas, fn)
                        print(f"Saved: {fn}")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if m_pos[1] < MENU_H: continue # Клик в зоне меню игнорируем
                
                if mode == 'fill':
                    flood_fill(canvas, adj_pos, color)
                elif mode == 'text':
                    text_active, text_pos, text_content = True, adj_pos, ""
                else:
                    drawing = True
                    start_pos, last_pos = adj_pos, adj_pos

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    if mode not in ['pencil', 'eraser']:
                        draw_shape(canvas, mode, color, start_pos, adj_pos, thickness)
                    drawing = False

            if event.type == pygame.MOUSEMOTION and drawing:
                if mode == 'pencil':
                    pygame.draw.line(canvas, color, last_pos, adj_pos, thickness)
                    last_pos = adj_pos
                elif mode == 'eraser':
                    pygame.draw.circle(canvas, (255, 255, 255), adj_pos, 20)

        # --- РЕНДЕРИНГ ---
        screen.fill((40, 40, 40)) # Темный фон меню
        screen.blit(canvas, (0, MENU_H)) # Рисуем холст ниже меню

        # Отрисовка текста меню
        f_ui = pygame.font.SysFont("Verdana", 13)
        ui_msg = f"MODE: {mode.upper()} | SIZE: {thickness} | P:Pencil L:Line F:Fill X:Text | R,C,S,T,U,D:Shapes | CTRL+S:Save"
        screen.blit(f_ui.render(ui_msg, True, (200, 200, 200)), (15, 20))

        # Превью фигуры (Ghost preview)
        if drawing and mode not in ['pencil', 'eraser']:
            # Рисуем превью на экран со смещением
            p_start = (start_pos[0], start_pos[1] + MENU_H)
            p_end = (m_pos[0], m_pos[1])
            draw_shape(screen, mode, color, p_start, p_end, thickness)

        # Превью текста
        if text_active:
            txt_surf = pygame.font.SysFont("Arial", 24).render(text_content + "|", True, color)
            screen.blit(txt_surf, (text_pos[0], text_pos[1] + MENU_H))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
