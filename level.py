from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_width, permanent_speed, kills_font
from sprite_groups import *
from tiles import StaticTile, Tile
from enemy import Enemy
from player import Player
from decoration import Sky, Clouds


class Level:
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift_x = 0
        self.number_of_enemies = 0

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_tile_list = import_cut_graphics('graphics/terrain/new_tiles.png')
        self.add_to_tile_group(terrain_layout, 'terrain')

        # enemy
        enemy_layout = import_csv_layout(level_data['enemy'])
        self.add_to_tile_group(enemy_layout, 'enemy')

        # player
        player_layout = import_csv_layout(level_data['player'])
        self.player_setup(player_layout)

        # constraint
        # enemy
        constraint_layout = import_csv_layout(level_data['enemy constraints'])
        self.add_to_tile_group(constraint_layout, 'enemy constraints')
        # player
        player_constraint_layout = import_csv_layout(level_data['player constraints'])
        self.add_to_tile_group(player_constraint_layout, 'player constraints')

        # decoration
        self.sky = Sky(12)
        level_width = len(terrain_layout[0]) * tile_size
        self.clouds = Clouds(200, level_width, 15)

    def add_to_tile_group(self, layout, sprite_type):
        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                if value != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if sprite_type == 'terrain':
                        tile_surface = self.terrain_tile_list[int(value)]
                        StaticTile(terrain_sprites, (tile_size, tile_size), x, y, tile_surface)

                    if sprite_type == 'grass and walls':
                        grass_tile_list = import_cut_graphics(
                            'graphics/decoration/grass_and_walls/grass_floor_deco.png')
                        tile_surface = grass_tile_list[int(value)]
                        StaticTile(grass_and_walls_sprites, (tile_size, tile_size), x, y, tile_surface)

                    if sprite_type == 'enemy':
                        if value == '0':  # red
                            Enemy(enemy_sprites, x, y + tile_size, 2.5, self.display_surface, 'red')
                        if value == '3':  # green
                            Enemy(enemy_sprites, x, y + tile_size, 2.5, self.display_surface, 'green')
                        if value == '4':  # black
                            Enemy(enemy_sprites, x, y + tile_size, 2.5, self.display_surface, 'black')
                        if value == '5':  # white
                            Enemy(enemy_sprites, x, y + tile_size, 2.5, self.display_surface, 'white')

                    if sprite_type == 'enemy constraints':
                        if value == '1':  # right
                            Tile(enemy_constraint_sprites, (1, tile_size), x + 70, y)
                        elif value == '2':  # left
                            Tile(enemy_constraint_sprites, (1, tile_size), x - 6, y)

                    if sprite_type == 'player constraints':
                        Tile(player_constraint_sprites, (tile_size, tile_size), x, y)

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

        if (screen_width // 2) > player_x > player_constraint_sprites.sprites()[0].rect.right + 7 * tile_size + 10\
                and direction_x < 0:
            self.world_shift_x = permanent_speed
            player.speed = 0
        elif (screen_width // 2) < player_x < player_constraint_sprites.sprites()[1].rect.left - 7 * tile_size - 10\
                and direction_x > 0:
            self.world_shift_x = -permanent_speed
            player.speed = 0
        else:
            self.world_shift_x = 0
            player.speed = permanent_speed

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
        # self.clouds.draw(self.display_surface, self.world_shift_x)

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
