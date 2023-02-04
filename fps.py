import pygame
from settings import screen_width, fps_font


class FPS:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.text = fps_font.render(str(self.clock.get_fps()), True, 'black')

    def render(self, display):
        self.text = fps_font.render(str(round(self.clock.get_fps())), True, 'black')
        display.blit(self.text, (screen_width - 60, 20))
