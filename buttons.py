import pygame
from settings import goal_font


class Button(pygame.sprite.Sprite):
    def __init__(self, group, x, y, surface_display):
        super().__init__(group)
        self.image = pygame.image.load('graphics/ui/e_button.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.text = goal_font.render('Enter', True, 'white')
        self.text_rect = self.text.get_rect(topleft=(x + 40, y + 5))
        self.text_rect.centery = self.rect.centery
        self.surface_display = surface_display

    def update(self, shift_x):
        self.rect.x += shift_x
        self.text_rect.x += shift_x
