__author__ = 'Yonatan Bachar'

import pygame
from settings import screen_height, screen_width, player_max_health
from sprite_groups import player_sprite, button_sprites
from level import Level
from game_data import level_list
from fps import FPS
from health_bar import HealthBar
from support import clear_level, play_music
from transitions import Fade
from menu import MainMenu
from timer import Timer

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Bubba\'s Adventures')
pygame.mouse.set_visible(False)


def main():
    jump_event = False
    attack_event = False
    button_event = False
    num_level = 0

    cursor_image = pygame.image.load('graphics/mouse/mouse_cursor.png').convert_alpha()
    music_list = ['sounds/menu_music.wav', 'sounds/game_music.wav', 'sounds/tutorial_music.wav']

    health_bar = HealthBar(screen)
    fps = FPS()
    fade = Fade()
    main_menu = MainMenu(screen)
    play_music(0, music_list)

    can_fade_out = False
    can_fade_in = False
    in_main_menu = True
    playing_tutorial = False
    playing_game = False
    create_level = True
    timer = None
    level = None
    pressed = ''

    run = True

    while run:
        if in_main_menu:  # the player is in the main menu
            cursor_image.set_alpha(255)
            check_button = main_menu.update(button_event, not can_fade_in)
            if check_button == 'play' or pressed == 'play':  # if the player pressed the play button
                pressed = 'play'
                cursor_image.set_alpha(0)
                can_fade_out = True
                if pygame.time.get_ticks() - main_menu.fade_timer > 1000:
                    timer = Timer()
                    playing_game = True  # send to game (level 1)
                    num_level = 1
                    in_main_menu = False
                    can_fade_in = True
                    can_fade_out = False
                    play_music(1, music_list)
            elif check_button == 'tutorial' or pressed == 'tutorial':  # if the player pressed the tutorial button
                pressed = 'tutorial'
                cursor_image.set_alpha(0)
                can_fade_out = True
                if pygame.time.get_ticks() - main_menu.fade_timer > 1000:
                    playing_tutorial = True  # send to tutorial
                    num_level = 0
                    in_main_menu = False
                    can_fade_in = True
                    can_fade_out = False
                    play_music(2, music_list)
                    pressed = ''

            button_sprites.update(button_event)
            button_sprites.draw(screen)

        else:  # the player is either in the game or in the tutorial
            if playing_game:  # if the player is in the game
                if num_level == 18 and level.next_level:
                    run = False

                if num_level == 1 and create_level:  # if the player came from the main menu
                    clear_level()
                    level = Level(level_list[num_level], screen, player_max_health, num_level)  # create level 1
                    create_level = False
                else:  # the player came from another level
                    if level.next_level:  # if the player is going to the next level
                        can_fade_out = True
                        if pygame.time.get_ticks() - level.reset_timer > 1000:
                            num_level += 1
                            temp_health = player_sprite.sprite.health
                            clear_level()  # clear the level
                            level = Level(level_list[num_level], screen,
                                          temp_health, num_level)  # create a new level x
                            can_fade_in = True
                            can_fade_out = False
            elif playing_tutorial:  # the player is in the tutorial
                if create_level:
                    clear_level()
                    level = Level(level_list[num_level], screen, player_max_health, num_level)  # create tutorial
                    create_level = False
                if level.next_level:
                    can_fade_out = True
                    if pygame.time.get_ticks() - level.reset_timer > 1000:
                        playing_tutorial = False
                        in_main_menu = True
                        create_level = True
                        can_fade_in = True
                        can_fade_out = False
                        play_music(0, music_list)

            if level:
                level.run()
                # player
                player_sprite.update(jump_event, attack_event)
                player_sprite.draw(screen)
                # health bar
                health_bar.update()
                health_bar.draw_health_bar()
                health_bar.update_hp(player_sprite.sprite.health)

        if timer is not None:
            if num_level != 18:
                timer.update()
            else:
                timer.draw(screen)

        fps.render(screen)
        jump_event = False
        attack_event = False
        button_event = False

        # fades
        if can_fade_out:
            fade.fade_out(screen)
        if can_fade_in:
            fade.fade_in(screen)
            if fade.fully_faded:
                fade.update()
                can_fade_in = False

        # event loop:
        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                    jump_event = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if not in_main_menu:
                        attack_event = True
                    else:
                        button_event = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    button_event = False

        screen.blit(cursor_image, pygame.mouse.get_pos())
        pygame.display.update()
        fps.clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
