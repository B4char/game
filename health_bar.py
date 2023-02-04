import pygame


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.image = pygame.image.load('graphics/ui/health_bar.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (10, 10)
        self.display_surface = surface

    def draw_health_bar(self):
        self.display_surface.blit(self.image, self.rect.bottomleft)
