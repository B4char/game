import pygame
from settings import screen_width, screen_height


class Fade(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surface = pygame.surface.Surface((screen_width, screen_height))
        self.surface.fill('black')
        self.alpha = 0
        self.fully_faded = False

    def fade_out(self, screen):
        self.surface.set_alpha(self.alpha)
        screen.blit(self.surface, (0, 0))
        pygame.display.update()
        if self.alpha < 300:
            self.alpha += 8

    def fade_in(self, screen):
        self.surface.set_alpha(self.alpha)
        screen.blit(self.surface, (0, 0))
        pygame.display.update()
        if self.alpha > 0:
            self.alpha -= 8
        else:
            self.fully_faded = True

    def update(self):
        self.fully_faded = False

