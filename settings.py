import pygame.font
pygame.font.init()

# screen variables
vertical_tile_number = 12
tile_size = 64
screen_height = 12*64
screen_width = 20*64

# text
fps_font = pygame.font.SysFont('Hackbot Free Trial', 30)
kills_font = pygame.font.SysFont('Hackbot Free Trial', 25)

# game variables
gravity = 0.7
permanent_speed = 4
player_health = 100
player_max_health = 100
