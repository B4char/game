import pygame
from settings import player_max_health


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.image = pygame.image.load('graphics/ui/health_bar.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (10, 10)
        self.hp_img = pygame.image.load('graphics/ui/hp.png').convert_alpha()
        self.hp_rect = self.hp_img.get_rect()
        self.hp_rect.bottomleft = (90, 25)
        self.display_surface = surface

    def draw_health_bar(self):
        self.display_surface.blit(self.hp_img, self.hp_rect.bottomleft)
        self.display_surface.blit(self.image, self.rect.bottomleft)

    def update_hp(self, health):
        self.hp_img = pygame.transform.scale(self.hp_img, (200/player_max_health*health, self.hp_rect.height))
        self.hp_rect = self.hp_img.get_rect()
        self.hp_rect.bottomleft = (90, 25)
