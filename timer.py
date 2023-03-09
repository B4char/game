import pygame
from settings import timer_font, screen_width


class Timer:
    def __init__(self):
        self.seconds = 0
        self.timer = pygame.time.get_ticks()
        self.text = timer_font.render(str(self.seconds), True, 'black')

    def update(self):
        self.seconds = (pygame.time.get_ticks() - self.timer)/1000

    def convert_time(self):
        sec = self.seconds
        sec = sec % (24 * 3600)
        hour = sec // 3600
        sec %= 3600
        minutes = sec // 60
        sec %= 60
        return "%02d:%02d:%02d" % (hour, minutes, sec)

    def draw(self, display):
        self.text = timer_font.render(self.convert_time(), True, 'black')
        display.blit(self.text, ((screen_width // 2) - (self.text.get_rect().width // 2), 20))
