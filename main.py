import pygame
from settings import screen_height, screen_width
from sprite_groups import player_sprite
from level import Level
from game_data import level_list
from fps import FPS
from health_bar import HealthBar
from support import clear_level
from transitions import Fade

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game')
# clock = pygame.time.Clock()

jump_event = False
attack_event = False
num_level = 0

level = Level(level_list[num_level], screen)
health_bar = HealthBar(screen)
fps = FPS()
fade = Fade()

can_fade_out = False
can_fade_in = False

run = True
while run:

    if level.next_level:
        can_fade_out = True
        if pygame.time.get_ticks() - level.reset_timer > 1000:
            num_level += 1
            clear_level()
            level = Level(level_list[num_level], screen)
            can_fade_in = True
            can_fade_out = False

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

    # fades
    if can_fade_out:
        fade.fade_out(screen)
    if can_fade_in:
        fade.fade_in(screen)
        if fade.fully_faded:
            fade.update()
            can_fade_in = False

    pygame.display.update()
    fps.clock.tick(60)

pygame.quit()
