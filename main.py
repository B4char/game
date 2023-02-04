import pygame
from settings import screen_height, screen_width
from sprite_groups import player_sprite
from level import Level
from game_data import *
from fps import FPS
from health_bar import HealthBar

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game')
# clock = pygame.time.Clock()

jump_event = False
attack_event = False

level = Level(level_1, screen)
health_bar = HealthBar(screen)
fps = FPS()

run = True
while run:

    jump_event = False
    attack_event = False

    # event loop:
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                jump_event = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                attack_event = True

    level.run()
    # player
    player_sprite.update(jump_event, attack_event)
    player_sprite.draw(screen)
    # health bar
    health_bar.update()
    health_bar.draw_health_bar()

    fps.render(screen)

    pygame.display.update()
    fps.clock.tick(60)

pygame.quit()
