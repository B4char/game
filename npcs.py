import pygame
from support import create_npc_animation_list
from sprite_groups import player_sprite


class Npc(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, color, group):
        super().__init__(group)
        self.animation_list = create_npc_animation_list(scale, color)
        self.frame_index = 0  # current frame in the animation list
        self.image = self.animation_list[self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect.y -= 32 - self.image.get_size()[1]
        self.npc_rect = pygame.rect.Rect(x - 50, y - 25, 100, 100)
        self.flip = True

        self.animation_timer = pygame.time.get_ticks()

    def animate(self):
        animation_speed = 260
        self.image = self.animation_list[self.frame_index]
        self.image = pygame.transform.flip(self.image, self.flip, False)

        if pygame.time.get_ticks() - self.animation_timer > animation_speed:
            self.animation_timer = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def face_player(self):
        if self.rect.centerx < player_sprite.sprite.rect.left:
            self.flip = False
        elif self.rect.centerx > player_sprite.sprite.rect.right:
            self.flip = True

    def update(self, shift_x):
        self.face_player()
        self.animate()
        self.rect.x += shift_x
        self.npc_rect.x += shift_x

