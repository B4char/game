import pygame.font
pygame.font.init()

# screen variables
vertical_tile_number = 12
tile_size = 64
screen_height = 12*64
screen_width = 20*64

# text
fps_font = pygame.font.Font('fonts/MinecraftRegular-Bmg3.ttf', 30)
kills_font = pygame.font.Font('fonts/MinecraftRegular-Bmg3.ttf', 25)
goal_font = pygame.font.Font('fonts/MinecraftRegular-Bmg3.ttf', 20)
main_font = pygame.font.Font('fonts/MinecraftRegular-Bmg3.ttf', 35)

# game variables
gravity = 0.7
permanent_speed = 4
player_max_health = 100
enemy_max_health = 100
