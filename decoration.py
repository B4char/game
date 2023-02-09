import pygame.image


class Sky:
    def __init__(self):
        self.rear = pygame.image.load('graphics/decoration/sky/background_rear.png').convert_alpha()
        self.rear = pygame.transform.scale(self.rear, (1440, 770))

    def draw(self, display_surface):
        display_surface.blit(self.rear, (0, 0))

