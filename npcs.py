import pygame
from support import create_npc_animation_list
from sprite_groups import player_sprite
from buttons import Button


class Npc(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, color, group, text, display_surface):
        super().__init__(group)
        self.npc_button_sprite = pygame.sprite.GroupSingle()
        self.display_surface = display_surface
        self.animation_list = create_npc_animation_list(scale, color)
        self.frame_index = 0  # current frame in the animation list
        self.image = self.animation_list[self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect.y -= 32 - self.image.get_size()[1]
        self.npc_rect = pygame.rect.Rect(x - 50, y - 25, 100, 100)
        self.flip = True

        self.animation_timer = pygame.time.get_ticks()

        Button(self.npc_button_sprite, x, y - 200, self.display_surface, text)

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

    def draw_text(self):
        self.display_surface.blit(self.npc_button_sprite.sprite.text, self.npc_button_sprite.sprite.text_rect)
        print(self.npc_button_sprite.sprite.text)

    def update(self, shift_x):
        self.face_player()
        self.animate()
        self.rect.x += shift_x
        self.npc_rect.x += shift_x
        self.npc_button_sprite.update(shift_x)

