import random

import pygame
from settings import gravity
from sprite_groups import terrain_sprites, player_sprite, health_orbs_sprites


class HealthOrb(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(health_orbs_sprites)
        self.image = pygame.image.load("graphics/character/health_orb.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.velocity = -6
        self.on_ground = False

    def drop_orb(self):
        self.velocity += gravity

    def check_collision(self):
        collision_sprites = pygame.sprite.spritecollide(self, terrain_sprites, False)
        if collision_sprites:
            for tile in collision_sprites:
                if self.rect.bottom >= tile.rect.top:
                    self.rect.bottom = tile.rect.top
                    self.velocity = 0
                    self.on_ground = True

        if pygame.Rect.colliderect(self.rect, player_sprite.sprite.rect):
            if not player_sprite.sprite.health >= 100:
                player_sprite.sprite.update_health(random.randint(4, 7))
                self.kill()

    def update(self, shift_x, display):
        # pygame.draw.rect(display, 'red', self.rect, 2)
        if not self.on_ground:
            self.drop_orb()
        self.check_collision()
        self.rect.y += self.velocity
        self.rect.x += shift_x
