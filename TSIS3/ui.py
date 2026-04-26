import pygame

pygame.font.init()

FONT = pygame.font.Font(None, 36)
BIG_FONT = pygame.font.Font(None, 64)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, (60, 60, 60), self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=10)

        text_surface = FONT.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


def draw_text(screen, text, x, y, color=(255, 255, 255), big=False):
    font = BIG_FONT if big else FONT
    img = font.render(text, True, color)
    screen.blit(img, (x, y))