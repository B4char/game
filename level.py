from random import randint
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_width, permanent_speed, kills_font
from sprite_groups import *
from tiles import StaticTile, Tile
from enemy import Enemy
from player import Player
from decoration import Sky


class Level:
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift_x = 0
        self.number_of_enemies = 0
        self.next_level = False

        # terrain:
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_tile_list = import_cut_graphics('graphics/terrain/new_tiles.png')
        self.add_to_tile_group(terrain_layout, 'terrain')

        # enemy:
        if not level_data.get('enemy') is None:
            enemy_layout = import_csv_layout(level_data['enemy'])
            self.add_to_tile_group(enemy_layout, 'enemy')

        # player:
        player_layout = import_csv_layout(level_data['player'])
        self.player_setup(player_layout)

        # constraint
        # enemy:
        if not level_data.get('enemy constraints') is None:
            enemy_constraint_layout = import_csv_layout(level_data['enemy constraints'])
            self.add_to_tile_group(enemy_constraint_layout, 'enemy constraints')
        # player:
        player_constraint_layout = import_csv_layout(level_data['player constraints'])
        self.add_to_tile_group(player_constraint_layout, 'player constraints')

        # decoration
        # stones:
        stone_layout = import_csv_layout(level_data['stones'])
        self.add_to_tile_group(stone_layout, 'stones')

        tree_layout = import_csv_layout(level_data['trees'])
        self.add_to_tile_group(tree_layout, 'trees')

        self.sky = Sky()
        mountain_tile = pygame.image.load('graphics/decoration/sky/background_middle.png').convert_alpha()
        mountain_tile = pygame.transform.scale(mountain_tile, (1440, 900))
        for x in range(0, 3):
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
                        Enemy(enemy_sprites, x, y + tile_size, 2.3, self.display_surface, 'white')
                        self.number_of_enemies += 1

                    if sprite_type == 'enemy constraints':
                        if value == '1':  # right
                            Tile(enemy_constraint_sprites, (1, tile_size), x + 70, y)
                        elif value == '2':  # left
                            Tile(enemy_constraint_sprites, (1, tile_size), x - 6, y)

                    if sprite_type == 'player constraints':
                        Tile(player_constraint_sprites, (tile_size, tile_size), x, y)

                    if sprite_type == 'stones':
                        tile_surface = self.terrain_tile_list[int(value)]
                        tile_surface = pygame.transform.flip(tile_surface, not bool(randint(0, 5)), False)
                        StaticTile(stone_sprites, (tile_size, tile_size), x + randint(-48, 48), y, tile_surface)

                    if sprite_type == 'trees':
                        tree_surface = pygame.image.load('graphics/decoration/tree.png').convert_alpha()
                        tree_surface = pygame.transform.scale(tree_surface, (tree_surface.get_width() * 2,
                                                                             tree_surface.get_height()*2))
                        StaticTile(tree_sprites, (tile_size, tile_size), x + randint(-48, 48), y - 192, tree_surface)

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                # player
                if value == '0':
                    Player(self.display_surface, (x, y - 10), player_sprite,
                           [terrain_sprites])
                # goal
                if value == '1':
                    hat_surface = pygame.image.load('graphics/character/player_end.png').convert_alpha()
                    StaticTile(goal_sprite, (tile_size, tile_size), x, y, hat_surface)

    def scroll_x(self):
        player = player_sprite.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player.is_alive:
            if (screen_width // 2) > player_x > player_constraint_sprites.sprites()[0].rect.right + 9 * tile_size + 10\
                    and direction_x < 0:
                self.world_shift_x = permanent_speed
                player.speed = 0
            elif (screen_width // 2) < player_x < player_constraint_sprites.sprites()[1].rect.left - 9 * tile_size - 10\
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

    def run(self):
        self.scroll_x()

        # text
        text, textRect = self.update_text()

        # sky
        self.sky.draw(self.display_surface)
        mountain_sprites.update(self.world_shift_x * 0.5)
        mountain_sprites.draw(self.display_surface)

        # decorations
        tree_sprites.update(self.world_shift_x)
        tree_sprites.draw(self.display_surface)
        stone_sprites.update(self.world_shift_x)
        stone_sprites.draw(self.display_surface)

        # enemy
        enemy_sprites.update(self.world_shift_x)
        enemy_sprites.draw(self.display_surface)
        enemy_constraint_sprites.update(self.world_shift_x)

        # terrain
        terrain_sprites.update(self.world_shift_x)
        terrain_sprites.draw(self.display_surface)

        # player sprites
        goal_sprite.update(self.world_shift_x)
        goal_sprite.draw(self.display_surface)
        player_constraint_sprites.update(self.world_shift_x)

        self.display_surface.blit(text, textRect)

        if self.number_of_enemies == 0:
            self.next_level = True
