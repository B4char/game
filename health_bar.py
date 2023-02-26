import pygame
from settings import player_max_health, kills_font


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.image = pygame.image.load('graphics/ui/health_bar.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (10, 10)
        self.hp_img = pygame.image.load('graphics/ui/hp.png').convert_alpha()
        self.hp_img_rect = self.hp_img.get_rect()
        self.hp_img_rect.bottomleft = (90, 25)
        self.display_surface = surface

    def draw_health_bar(self):
        self.display_surface.blit(self.hp_img, self.hp_img_rect.bottomleft)
        self.display_surface.blit(self.image, self.rect.bottomleft)

    def update_hp(self, health):
        self.hp_img = pygame.transform.scale(self.hp_img, (200 / player_max_health * health, self.hp_img_rect.height))
        self.hp_img_rect = self.hp_img.get_rect()
        self.hp_img_rect.bottomleft = (90, 25)
        text = kills_font.render(str(health) + "/" + str(player_max_health), True, 'black')
        if health < 100:
            offset_x = 10
        else:
            offset_x = 0
        self.display_surface.blit(text, (137 + offset_x, 22))
