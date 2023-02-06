import pygame

# setup sprite groups
# particles:
player_attack_particles = pygame.sprite.GroupSingle()

# player:
player_sprite = pygame.sprite.GroupSingle()
goal_sprite = pygame.sprite.Group()
player_constraint_sprites = pygame.sprite.Group()

# enemy
enemy_sprites = pygame.sprite.Group()
enemy_constraint_sprites = pygame.sprite.Group()

# level
terrain_sprites = pygame.sprite.Group()
grass_and_walls_sprites = pygame.sprite.Group()
cloud_sprites = pygame.sprite.Group()
