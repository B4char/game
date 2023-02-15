import pygame

pygame.mixer.init(44100, -16, 2, 512)
pygame.mixer.pre_init(44100, -16, 2, 512)

hit_sound = pygame.mixer.Sound('sounds/hit_sound.wav')
hit_sound.set_volume(0.7)
jump_sound = pygame.mixer.Sound('sounds/jump_sound.wav')
jump_sound.set_volume(0.7)
button_sound = pygame.mixer.Sound('sounds/button_sound.wav')

