import pygame
from decoration import Clouds
from support import create_npc_animation_list, create_clouds
from sprite_groups import button_sprites, cloud_sprites
from buttons import MenuButton
from random import randint


class MainMenu(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.fade_timer = pygame.time.get_ticks()
        self.frame_index = 0
        self.animation_list = create_npc_animation_list(2.3, 'purple')
        self.sky = pygame.surface.Surface((1280, 770))
        self.sky.fill((92, 211, 255))

        self.mountain = pygame.image.load('graphics/decoration/sky/background_middle.png')
        self.mountain1 = pygame.transform.scale(self.mountain, (1440, 980))
        self.mountain2 = pygame.transform.scale(self.mountain, (1440, 980))
        self.mountain_rect1 = self.mountain1.get_rect(topleft=(0, -100))
        self.mountain_rect2 = self.mountain2.get_rect(topleft=(1440, -100))

        self.grass1 = pygame.image.load('graphics/decoration/grass.png')
        self.grass2 = pygame.image.load('graphics/decoration/grass.png')
        self.grass3 = pygame.image.load('graphics/decoration/grass.png')
        self.grass_rect1 = self.grass1.get_rect(topleft=(0, 664))
        self.grass_rect2 = self.grass2.get_rect(topleft=(720, 664))
        self.grass_rect3 = self.grass3.get_rect(topleft=(1440, 664))

        self.player_img = self.animation_list[self.frame_index]
        self.update_time = pygame.time.get_ticks()

        self.play_button = MenuButton(640 - 300 * 0.75 // 2, 200, button_sprites, 'play')
        self.tutorial_button = MenuButton(640 - 420 * 0.75 // 2, 325, button_sprites, 'tutorial')

        create_clouds()

    def animate(self):
        animation_speed = 150
        self.player_img = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_speed:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def scroll_x(self):
        self.mountain_rect1.x -= 1
        self.mountain_rect2.x -= 1
        self.grass_rect1.x -= 2
        self.grass_rect2.x -= 2
        self.grass_rect3.x -= 2

        if self.mountain_rect1.right <= 0:
            self.mountain_rect1.x = 1440
        elif self.mountain_rect2.right <= 0:
            self.mountain_rect2.x = 1440
        if self.grass_rect1.right <= 0:
            self.grass_rect1.x = 1440
        elif self.grass_rect2.right <= 0:
            self.grass_rect2.x = 1440
        elif self.grass_rect3.right <= 0:
            self.grass_rect3.x = 1440

    def update(self, pressed, in_transition) -> str:
        self.scroll_x()
        self.screen.blit(self.sky, (0, 0))
        cloud_sprites.update(-0.5)
        cloud_sprites.draw(self.screen)
        self.screen.blit(self.mountain1, self.mountain_rect1.topleft)
        self.screen.blit(self.mountain2, self.mountain_rect2.topleft)
        self.screen.blit(self.grass1, self.grass_rect1.topleft)
        self.screen.blit(self.grass2, self.grass_rect2.topleft)
        self.screen.blit(self.grass3, self.grass_rect3.topleft)
        self.screen.blit(self.player_img, (640 - self.player_img.get_width() // 2, 600))
        self.animate()
        if self.play_button.check_pressed(pressed, in_transition) == 'play':
            self.fade_timer = pygame.time.get_ticks()
            return 'play'
        elif self.tutorial_button.check_pressed(pressed, in_transition) == 'tutorial':
            self.fade_timer = pygame.time.get_ticks()
            return 'tutorial'
