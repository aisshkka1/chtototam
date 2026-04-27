import pygame

class Button:
    def __init__(self, x, y, width, height, text, color=(200, 200, 200)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont("Verdana", 20)

    def draw(self, surface):
        # Рисуем саму кнопку
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2) # Рамка
        # Рисуем текст
        txt_surf = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(txt_surf, (self.rect.centerx - txt_surf.get_width() // 2, 
                               self.rect.centery - txt_surf.get_height() // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class TextInput:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.font = pygame.font.SysFont("Verdana", 24)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                pass
            else:
                if len(self.text) < 15:
                    self.text += event.unicode

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        txt_surf = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(txt_surf, (self.rect.x + 5, self.rect.y + 5))