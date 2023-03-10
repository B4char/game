from random import randint
from support import import_csv_layout, import_cut_graphics, create_clouds
from settings import tile_size, screen_width, permanent_speed, kills_font
from sprite_groups import *
from tiles import StaticTile, Tile
from enemy import Enemy
from player import Player
from decoration import Sky
from buttons import Button
from npcs import Npc


class Level:
    def __init__(self, level_data, surface, health, current_level):
        # general setup
        self.current_level = current_level
        self.display_surface = surface
        self.world_shift_x = 0
        self.number_of_enemies = 0
        self.draw_goal = False
        self.draw_text = False
        self.play_tutorial = False
        self.back_to_lobby = False
        self.next_level = False
        self.updated = False
        self.tutorial_updated = False
        self.reset_timer = pygame.time.get_ticks()
        self.tutorial_timer = pygame.time.get_ticks()
        self.player_health = health
        self.show_text = False
        self.text_type = 'move'
        self.tutorial_dialogue = ['move', 'attack', 'none']
        self.counter = 0

        # terrain:
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_tile_list = import_cut_graphics('graphics/terrain/new_tiles.png')
        self.add_to_tile_group(terrain_layout, 'terrain')

        # enemy:
        if not level_data.get('enemy') is None:
            enemy_layout = import_csv_layout(level_data['enemy'])
            self.add_to_tile_group(enemy_layout, 'enemy')

        # player:
        if not level_data.get('player') is None:
            player_layout = import_csv_layout(level_data['player'])
            self.player_setup(player_layout)

        # border
        # enemy:
        if not level_data.get('enemy borders') is None:
            enemy_border_layout = import_csv_layout(level_data['enemy borders'])
            self.add_to_tile_group(enemy_border_layout, 'enemy borders')
        # player:
        if not level_data.get('player borders') is None:
            player_border_layout = import_csv_layout(level_data['player borders'])
            self.add_to_tile_group(player_border_layout, 'player borders')

        # decoration
        # stones:
        if not level_data.get('stones') is None:
            stone_layout = import_csv_layout(level_data['stones'])
            self.add_to_tile_group(stone_layout, 'stones')

        if not level_data.get('trees') is None:
            tree_layout = import_csv_layout(level_data['trees'])
            self.add_to_tile_group(tree_layout, 'trees')

        if not level_data.get('npc') is None:
            npc_layout = import_csv_layout(level_data['npc'])
            self.add_to_tile_group(npc_layout, 'npc')

        self.sky = Sky()
        create_clouds()
        mountain_tile = pygame.image.load('graphics/decoration/sky/background_middle.png').convert_alpha()
        mountain_tile = pygame.transform.scale(mountain_tile, (1440, 900))
        for x in range(0, 2):
            StaticTile(mountain_sprites, (0, 0), x * mountain_tile.get_width(), - 120, mountain_tile)

    def add_to_tile_group(self, layout, sprite_type):
        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                if value != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if sprite_type == 'terrain':
                        tile_surface = self.terrain_tile_list[int(value)]
                        StaticTile(terrain_sprites, (tile_size, tile_size), x, y, tile_surface)

                    if sprite_type == 'enemy':
                        if value == '0':
                            Enemy(enemy_sprites, x, y, 2.3, self.display_surface, 'red')
                        if value == '1':
                            Enemy(enemy_sprites, x, y, 2.3, self.display_surface, 'green')
                        if value == '2':
                            Enemy(enemy_sprites, x, y, 2.3, self.display_surface, 'black')
                        if value == '3':
                            Enemy(enemy_sprites, x, y, 2.3, self.display_surface, 'white')
                        self.number_of_enemies += 1

                    if sprite_type == 'enemy borders':
                        if value == '4':  # right
                            Tile(enemy_borders_sprites, (1, tile_size), x + 70, y)
                        elif value == '5':  # left
                            Tile(enemy_borders_sprites, (1, tile_size), x - 6, y)

                    if sprite_type == 'player borders':
                        Tile(player_borders_sprites, (tile_size, tile_size), x, y)

                    if sprite_type == 'stones':
                        tile_surface = self.terrain_tile_list[int(value)]
                        tile_surface = pygame.transform.flip(tile_surface, not bool(randint(0, 5)), False)
                        StaticTile(stone_sprites, (tile_size, tile_size), x + randint(-48, 48), y, tile_surface)

                    if sprite_type == 'trees':
                        tree_surface = pygame.image.load('graphics/decoration/tree.png').convert_alpha()
                        tree_surface = pygame.transform.scale(tree_surface, (tree_surface.get_width() * 2,
                                                                             tree_surface.get_height()*2))
                        StaticTile(tree_sprites, (tile_size, tile_size), x + randint(-48, 48), y - 192, tree_surface)

                    if sprite_type == 'npc':
                        if value == '1':
                            Npc(x, y, 2.3, 'blue', npc_sprite, self.display_surface)
                            Button(npc_button_sprite, x - 77, y - 35, self.display_surface, 'How to play')

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                # player
                if value == '0':
                    Player(self.display_surface, (x, y - 10), player_sprite,
                           [terrain_sprites], self.player_health)
                # goal
                if value == '1':
                    goal_surface = pygame.image.load('graphics/character/player_end.png').convert_alpha()
                    goal_surface = pygame.transform.scale(goal_surface, (int(goal_surface.get_width() * 1.18),
                                                                         int(goal_surface.get_height() * 1.18)))
                    if self.current_level == 0:
                        text = 'Back to menu'
                        offset_x = 54
                        goal_surface = pygame.transform.flip(goal_surface, True, False)
                    elif self.current_level == 18:
                        text = 'Exit game'
                        offset_x = 37
                    else:
                        text = 'Next level'
                        offset_x = 40
                    StaticTile(goal_sprite, (tile_size, tile_size), x, y - 11, goal_surface)
                    Button(goal_button_sprite, x - offset_x, y - 35, self.display_surface, text)

    def scroll_x(self):
        player = player_sprite.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player.is_alive:
            if (screen_width // 2) > player_x > player_borders_sprites.sprites()[0].rect.right + 9 * tile_size + 10\
                    and direction_x < 0:
                self.world_shift_x = permanent_speed
                player.speed = 0
            elif (screen_width // 2) < player_x < player_borders_sprites.sprites()[1].rect.left - 9 * tile_size - 10\
                    and direction_x > 0:
                self.world_shift_x = -permanent_speed
                player.speed = 0
            else:
                self.world_shift_x = 0
                player.speed = permanent_speed
        else:
            self.world_shift_x = 0

    def update_text(self):
        self.number_of_enemies = 0
        for enemy in enemy_sprites.sprites():
            if enemy.is_alive:
                self.number_of_enemies += 1
        text = kills_font.render(str(self.number_of_enemies), True, 'black')
        textRect = text.get_rect()
        textRect.center = (152, 81)
        return text, textRect

    def check_goal_collision(self):
        if self.number_of_enemies == 0 or self.current_level == 0:
            if pygame.sprite.spritecollide(player_sprite.sprite, goal_sprite, False):
                self.draw_goal = True

                keys = pygame.key.get_pressed()
                if keys[pygame.K_e]:
                    if not self.updated:
                        self.reset_timer = pygame.time.get_ticks()
                        self.next_level = True
                        self.updated = True
            else:
                self.draw_goal = False

    def check_npc_collision(self):
        if pygame.Rect.colliderect(player_sprite.sprite.rect, npc_sprite.sprite.npc_rect) and not self.tutorial_updated:
            self.draw_text = True
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                if not self.tutorial_updated:
                    self.tutorial_updated = True
                    self.show_text = True
        else:
            self.draw_text = False

    def run(self):
        self.scroll_x()
        if goal_sprite:
            self.check_goal_collision()
        if npc_sprite:
            self.check_npc_collision()

        # text
        text, textRect = self.update_text()

        if not self.tutorial_updated:
            self.tutorial_timer = pygame.time.get_ticks()

        # sky
        self.sky.draw(self.display_surface)

        cloud_sprites.update(self.world_shift_x * 0.125)
        cloud_sprites.draw(self.display_surface)

        mountain_sprites.update(self.world_shift_x * 0.5)
        mountain_sprites.draw(self.display_surface)

        # decorations
        tree_sprites.update(self.world_shift_x)
        tree_sprites.draw(self.display_surface)
        stone_sprites.update(self.world_shift_x)
        stone_sprites.draw(self.display_surface)

        # enemies
        enemy_sprites.update(self.world_shift_x)
        enemy_sprites.draw(self.display_surface)
        enemy_borders_sprites.update(self.world_shift_x)
        # enemy_borders_sprites.draw(self.display_surface)

        # NPCs
        if pygame.time.get_ticks() - self.tutorial_timer > 6000:
            self.counter += 1
            self.text_type = self.tutorial_dialogue[self.counter]
            self.tutorial_timer = pygame.time.get_ticks()
        npc_sprite.update(self.world_shift_x, self.show_text, self.tutorial_dialogue[self.counter])
        npc_sprite.draw(self.display_surface)
        if self.counter == 2:
            self.counter = 0
            self.tutorial_updated = False
            self.show_text = False

        # terrain
        terrain_sprites.update(self.world_shift_x)
        terrain_sprites.draw(self.display_surface)

        health_orbs_sprites.update(self.world_shift_x, self.display_surface)
        health_orbs_sprites.draw(self.display_surface)

        # player sprites
        goal_sprite.update(self.world_shift_x)
        goal_sprite.draw(self.display_surface)
        player_borders_sprites.update(self.world_shift_x)

        self.display_surface.blit(text, textRect)

        if self.draw_goal:
            goal_button_sprite.draw(self.display_surface)
            self.display_surface.blit(goal_button_sprite.sprite.text, goal_button_sprite.sprite.text_rect)
        goal_button_sprite.update(self.world_shift_x)

        if self.draw_text:
            npc_button_sprite.draw(self.display_surface)
            self.display_surface.blit(npc_button_sprite.sprite.text, npc_button_sprite.sprite.text_rect)
        npc_button_sprite.update(self.world_shift_x)

        for particle in particles_sprite.sprites():
            particle.update(player_sprite.sprite.flip, self.display_surface, self.world_shift_x)
        particles_sprite.draw(self.display_surface)
