import pygame as pg
import pygame.font

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

COLORS = [GREEN, WHITE]

class Button:
    def __init__(self, screen, rect, message="Button", action=print):
        self.screen = screen

        self.action = action

        self.color_index = 0
        self.font = pygame.font.SysFont(None, 48)

        self.rect = rect
        self.message = message;
        self.image = self.font.render(message, True, COLORS[self.color_index], COLORS[(self.color_index + 1) % 2])
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.rect.center
        self.rect = self.image_rect
        self.x, self.y, self.w, self.h = self.image_rect

    def print(self):
        print(self.x, self.y)

    def is_hovering(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        return self.x <= mouse_x <= self.x + self.w and self.y <= mouse_y <= self.y + self.h

    def update(self):
        if self.is_hovering():
            self.color_index = 1
        else:
            self.color_index = 0
        self.image = self.font.render(self.message, True, COLORS[self.color_index], COLORS[(self.color_index + 1) % 2])
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.rect.center

    def draw(self):
        # self.screen.fill(self.color, self.rect)
        self.screen.blit(self.image, self.image_rect)

