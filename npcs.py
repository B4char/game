import pygame
from support import create_npc_animation_list
from sprite_groups import player_sprite, bubble_text_sprite
from settings import tutorial_font


class Npc(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, color, group, screen):
        super().__init__(group)
        self.screen = screen
        self.animation_list = create_npc_animation_list(scale, color)
        self.frame_index = 0  # current frame in the animation list
        self.image = self.animation_list[self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect.y -= 32 - self.image.get_size()[1]
        self.npc_rect = pygame.rect.Rect(x - 50, y - 25, 100, 100)
        self.flip = True

        self.animation_timer = pygame.time.get_ticks()

        self.text_bubble = TextBubble(x, y, screen)

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

    def update(self, shift_x, show_text, text_type):
        self.face_player()
        self.animate()
        self.rect.x += shift_x
        self.npc_rect.x += shift_x
        if show_text:
            self.text_bubble.draw()
        self.text_bubble.update(shift_x, text_type)


class TextBubble(pygame.sprite.Sprite):
    def __init__(self, x, y, screen):
        super().__init__(bubble_text_sprite)
        self.x = x
        self.y = y
        self.text = None
        self.text1 = None
        self.text2 = None
        self.image = pygame.image.load('graphics/npc/text_bubble1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, (self.x - 20, 285))
        if self.text is None:
            self.screen.blit(self.text1, (self.x + 55, 305))
            self.screen.blit(self.text2, (self.x + 146, 360))
        elif self.text1 is None or self.text2 is None:
            self.screen.blit(self.text, (self.x + 55, 305))

    def update(self, shift_x, text_type):
        if text_type == 'move':
            self.image = pygame.image.load('graphics/npc/text_bubble1.png').convert_alpha()
            self.text = None
            text1 = 'To move press:'
            text2 = 'or'
            self.text1 = tutorial_font.render(str(text1), True, 'black')
            self.text2 = tutorial_font.render(str(text2), True, 'black')
        elif text_type == 'attack':
            self.text1 = None
            self.text2 = None
            self.image = pygame.image.load('graphics/npc/text_bubble2.png').convert_alpha()
            text = 'To attack press:'
            self.text = tutorial_font.render(str(text), True, 'black')
        else:
            self.image.set_alpha(0)
        self.rect.x += shift_x
