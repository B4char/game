import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, group, size, x, y):
        super().__init__(group)
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.old_rect = self.rect.copy()

    def update(self, shift_x):
        self.old_rect = self.rect.copy()
        self.rect.x += shift_x


class StaticTile(Tile):
    def __init__(self, group, size, x, y, surface):
        super().__init__(group, size, x, y)
        self.image = surface
