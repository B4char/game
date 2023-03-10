from csv import reader
from random import randint

import pygame.image

from decoration import Clouds
from settings import tile_size
from os import listdir, walk
from sprite_groups import *


def import_folder(path, scale):
    surface_list = []

    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            image_surface = pygame.transform.scale(image_surface, (int(image_surface.get_width() * scale),
                                                                   int(image_surface.get_height() * scale)))
            surface_list.append(image_surface)

    return surface_list


def import_csv_layout(path):
    terrain_map = []

    with open(path) as level_map:
        level = reader(level_map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))

    return terrain_map


def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surface = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
            new_surface.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surface)

    return cut_tiles


def create_player_animation_list(scale):
    animation_images = []
    animation_types = ['idle', 'run', 'jump', 'fall', 'attack', 'death']
    for animation in animation_types:
        temp_list = []
        action_length = len(listdir(f'graphics/character/{animation}'))
        for i in range(action_length):
            animation_img = pygame.image.load(f'graphics/character/{animation}/{i}.png').convert_alpha()
            animation_img = pygame.transform.scale(animation_img, (int(animation_img.get_width() * scale),
                                                                   int(animation_img.get_height() * scale)))
            temp_list.append(animation_img)
        animation_images.append(temp_list)
    return animation_images


def create_enemy_animation_list(scale, color):
    animation_images = []
    animation_types = ['idle', 'walk', 'fall', 'attack', 'death']
    for animation in animation_types:
        temp_list = []
        action_length = len(listdir(f'graphics/enemy/{color}/{animation}'))
        for i in range(action_length):
            animation_img = pygame.image.load(f'graphics/enemy/{color}/{animation}/{i}.png').convert_alpha()
            animation_img = pygame.transform.scale(animation_img, (int(animation_img.get_width() * scale),
                                                                   int(animation_img.get_height() * scale)))
            temp_list.append(animation_img)
        animation_images.append(temp_list)
    return animation_images


def create_npc_animation_list(scale, color):
    animation_images = []
    action_length = len(listdir(f'graphics/npc/{color}'))
    for i in range(action_length):
        animation_img = pygame.image.load(f'graphics/npc/{color}/{i}.png').convert_alpha()
        animation_img = pygame.transform.scale(animation_img, (int(animation_img.get_width() * scale),
                                                               int(animation_img.get_height() * scale)))
        animation_images.append(animation_img)
    return animation_images


def create_attack_particles(scale):
    particles_list = []
    action_length = len(listdir('graphics/particles/attack_particles'))
    for i in range(action_length):
        animation_img = pygame.image.load(f'graphics/particles/attack_particles/{i}.png').convert_alpha()
        animation_img = pygame.transform.scale(animation_img, (int(animation_img.get_width() * scale),
                                                               int(animation_img.get_height() * scale)))
        particles_list.append(animation_img)
    return particles_list


def create_particles(scale):
    particles_images = []
    particles_types = ['jump', 'fall', 'run']
    for particle in particles_types:
        temp_list = []
        action_length = len(listdir(f'graphics/particles/{particle}'))
        for i in range(action_length):
            particle_img = pygame.image.load(f'graphics/particles/{particle}/{i}.png').convert_alpha()
            particle_img = pygame.transform.scale(particle_img, (int(particle_img.get_width() * scale),
                                                                 int(particle_img.get_height() * scale)))
            temp_list.append(particle_img)
        particles_images.append(temp_list)
    return particles_images


def create_clouds():
    count_clouds = 0
    while count_clouds < 8:
        pos_x = randint(50, 1300)
        pos_y = randint(30, 400)
        new_cloud = Clouds(pos_x, pos_y)
        if cloud_sprites:
            if new_cloud:
                if not pygame.sprite.spritecollide(new_cloud, cloud_sprites, False):
                    count_clouds += 1
                    cloud_sprites.add(new_cloud)
        else:
            count_clouds += 1
            cloud_sprites.add(new_cloud)


def play_music(music, music_list):
    if music == 0:
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.load(music_list[0])
        pygame.mixer.music.set_volume(0.135)
    elif music == 1:
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.load(music_list[1])
        pygame.mixer.music.set_volume(0.135)
    elif music == 2:
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.load(music_list[2])
        pygame.mixer.music.set_volume(0.135)
    pygame.mixer.music.play(-1)


def clear_level():
    enemy_sprites.empty()
    terrain_sprites.empty()
    player_sprite.empty()
    enemy_borders_sprites.empty()
    player_borders_sprites.empty()
    goal_sprite.empty()
    stone_sprites.empty()
    tree_sprites.empty()
    npc_button_sprite.empty()
    npc_sprite.empty()
    goal_button_sprite.empty()
    cloud_sprites.empty()
    mountain_sprites.empty()
    health_orbs_sprites.empty()
