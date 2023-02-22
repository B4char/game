from random import randint
import pygame.image


class Sky:
    def __init__(self):
        self.rear = pygame.image.load('graphics/decoration/sky/background_rear.png').convert_alpha()
        self.rear = pygame.transform.scale(self.rear, (1440, 770))

    def draw(self, display_surface):
        display_surface.blit(self.rear, (0, 0))


class Clouds(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load('graphics/decoration/clouds/{}.png'.format(str(randint(1, 10))))
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.5),
                                                         int(self.image.get_height()*0.5)))
        if not bool(randint(0, 3)):
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        self.rect.width += 30
        self.rect.height += 30
        self.shift_x = 0

    def update(self, shift_x):
        self.shift_x += shift_x
        if self.shift_x % 1 == 0 and self.shift_x != 0:
            self.rect.x += self.shift_x
            self.shift_x = 0

        if self.rect.right < 0:
            self.rect.left = 1280



