import pygame
from settings import screen_height, screen_width, player_max_health
from sprite_groups import player_sprite, button_sprites
from level import Level
from game_data import level_list
from fps import FPS
from health_bar import HealthBar
from support import clear_level
from transitions import Fade
from menu import MainMenu

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game')

jump_event = False
attack_event = False
button_event = False
num_level = 0

can_play = True

music_list = ['sounds/game_music.wav', 'sounds/menu_music.wav', 'sounds/tutorial_music.wav']
pygame.mixer.music.set_volume(0.135)

health_bar = HealthBar(screen)
fps = FPS()
fade = Fade()
main_menu = MainMenu(screen)

can_fade_out = False
can_fade_in = False
in_main_menu = True
playing_tutorial = False
playing_game = False
create_level = True
fade_timer = pygame.time.get_ticks()
level = None
checked = ''

run = True
while run:
    if in_main_menu:  # the player is in the main menu
        check = main_menu.update(button_event)
        if check == 'play' or checked == 'play':  # if the player pressed the play button
            checked = 'play'
            can_fade_out = True
            if pygame.time.get_ticks() - main_menu.fade_timer > 1000:
                playing_game = True  # send to game
                num_level = 1
                in_main_menu = False
                can_fade_in = True
                can_fade_out = False
                can_play = True
                pygame.mixer.music.fadeout(1000)
        elif check == 'tutorial' or checked == 'tutorial':  # if the player pressed the tutorial button
            checked = 'tutorial'
            can_fade_out = True
            if pygame.time.get_ticks() - main_menu.fade_timer > 1000:
                playing_tutorial = True  # send to tutorial
                num_level = 0
                in_main_menu = False
                can_fade_in = True
                can_fade_out = False
                can_play = True
                pygame.mixer.music.fadeout(1000)

        button_sprites.update(button_event)
        button_sprites.draw(screen)

    else:  # the player is either in the game or in the tutorial
        if playing_game:  # if the player is in the game
            if num_level == 1 and create_level:  # if the player came from the main menu
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
                level = Level(level_list[num_level], screen, player_max_health, num_level)  # create tutorial
                create_level = False
            if level.next_level:
                num_level = 0
                playing_tutorial = False
                playing_game = True
                create_level = False

        if level:
            level.run()
            # player
            player_sprite.update(jump_event, attack_event)
            player_sprite.draw(screen)
            # health bar
            health_bar.update()
            health_bar.draw_health_bar()
            health_bar.update_hp(player_sprite.sprite.health)

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

    if can_play:
        if in_main_menu:
            pygame.mixer.music.load(music_list[1])
        else:
            if playing_tutorial:
                pygame.mixer.music.load(music_list[2])
            else:
                pygame.mixer.music.load(music_list[0])
        pygame.mixer.music.play(-1)
        can_play = False

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
                if not in_main_menu:
                    attack_event = True
                else:
                    button_event = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                button_event = False

    pygame.display.update()
    fps.clock.tick(60)

pygame.quit()
