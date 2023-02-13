import pygame
from settings import goal_font


class Button(pygame.sprite.Sprite):
    def __init__(self, group, x, y, surface_display, text):
        super().__init__(group)
        self.image = pygame.image.load('graphics/ui/e_button.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.text = goal_font.render(text, True, 'white')
        self.text_rect = self.text.get_rect(topleft=(x + 40, y + 5))
        self.text_rect.centery = self.rect.centery
        self.surface_display = surface_display

    def update(self, shift_x):
        self.rect.x += shift_x
        self.text_rect.x += shift_x


class MenuButton(pygame.sprite.Sprite):
    def __init__(self, x, y, group, button):
        super().__init__(group)
        self.type = button
        self.image = pygame.image.load(f'graphics/buttons/{button}.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 0.75, self.image.get_height() * 0.75))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = self.rect.topleft[0]
        self.y = self.rect.topleft[1]

    def check_pressed(self, pressed):
        if self.x <= pygame.mouse.get_pos()[0] <= self.x + self.rect.width and\
                self.y <= pygame.mouse.get_pos()[1] <= self.y + self.rect.height:
            self.image.set_alpha(235)
            if pressed:
                if self.type == 'play':
                    return 'play'
                elif self.type == 'tutorial':
                    return 'tutorial'
        else:
            self.image.set_alpha(255)
