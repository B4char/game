import pygame.image
from sprite_groups import cloud_sprites
from settings import vertical_tile_number, tile_size, screen_width
from tiles import StaticTile
from support import import_folder
from random import choice, randint


class Sky:
    def __init__(self, horizon):
        self.top = pygame.image.load('graphics/decoration/sky/sky_top.png').convert()
        self.horizon = horizon

        # stretch
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))

    def draw(self, surface):
        for row in range(vertical_tile_number):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top, (0, y))


class Clouds:
    def __init__(self, horizon, level_width, cloud_number):
        cloud_surface_list = import_folder('graphics/decoration/clouds', 1)
        min_x = -screen_width
        max_x = level_width + screen_width
        min_y = 0
        max_y = horizon

        for cloud in range(cloud_number):
            cloud = choice(cloud_surface_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            StaticTile(cloud_sprites, (0, 0), x, y, cloud)

    def draw(self, surface, shift_x):
        cloud_sprites.update(shift_x)
        cloud_sprites.draw(surface)
