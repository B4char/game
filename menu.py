import pygame
from support import create_npc_animation_list
from sprite_groups import button_sprites
from buttons import MenuButton


class MainMenu(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.fade_timer = pygame.time.get_ticks()
        self.frame_index = 0
        self.animation_list = create_npc_animation_list(2.3, 'light_blue')
        self.sky = pygame.surface.Surface((1280, 770))
        self.sky.fill((92, 211, 255))

        self.mountain = pygame.image.load('graphics/decoration/sky/background_middle.png')
        self.mountain1 = pygame.transform.scale(self.mountain, (1440, 770))
        self.mountain2 = pygame.transform.scale(self.mountain, (1440, 770))
        self.mountain_rect1 = self.mountain1.get_rect(topleft=(0, 0))
        self.mountain_rect2 = self.mountain2.get_rect(topleft=(1440, 0))

        self.grass1 = pygame.image.load('graphics/decoration/grass.png')
        self.grass2 = pygame.image.load('graphics/decoration/grass.png')
        self.grass_rect1 = self.grass1.get_rect(topleft=(0, 600))
        self.grass_rect2 = self.grass2.get_rect(topleft=(1440, 600))

        self.player_img = self.animation_list[self.frame_index]
        self.update_time = pygame.time.get_ticks()

        self.play_button = MenuButton(640 - 300 * 0.75 // 2, 200, button_sprites, 'play')
        self.tutorial_button = MenuButton(640 - 500 * 0.75 // 2, 325, button_sprites, 'tutorial')

    def animate(self):
        animation_speed = 150

        self.player_img = self.animation_list[self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_speed:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def scroll_x(self):
        self.mountain_rect1.update(self.mountain_rect1.x - 1, self.mountain_rect1.y, self.mountain_rect1.width, self.mountain_rect1.height)
        self.mountain_rect2.update(self.mountain_rect2.x - 1, self.mountain_rect2.y, self.mountain_rect2.width, self.mountain_rect2.height)
        self.grass_rect1.update(self.grass_rect1.x - 2, self.grass_rect1.y, self.grass_rect1.width, self.grass_rect1.height)
        self.grass_rect2.update(self.grass_rect2.x - 2, self.grass_rect2.y, self.grass_rect2.width, self.grass_rect2.height)

        if self.mountain_rect1.right <= 0:
            self.mountain_rect1.x = 1440
        elif self.mountain_rect2.right <= 0:
            self.mountain_rect2.x = 1440
        if self.grass_rect1.right <= 0:
            self.grass_rect1.x = 1440
        elif self.grass_rect2.right <= 0:
            self.grass_rect2.x = 1440

    def update(self, pressed) -> str:
        self.scroll_x()
        self.screen.blit(self.sky, (0, 0))
        self.screen.blit(self.mountain1, self.mountain_rect1.topleft)
        self.screen.blit(self.mountain2, self.mountain_rect2.topleft)
        self.screen.blit(self.grass1, self.grass_rect1.topleft)
        self.screen.blit(self.grass2, self.grass_rect2.topleft)
        self.screen.blit(self.player_img, (640 - self.player_img.get_width() // 2, 536))
        self.animate()
        if self.play_button.check_pressed(pressed) == 'play':
            self.fade_timer = pygame.time.get_ticks()
            return 'play'
        elif self.tutorial_button.check_pressed(pressed) == 'tutorial':
            self.fade_timer = pygame.time.get_ticks()
            return 'tutorial'
