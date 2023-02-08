import pygame

# setup sprite groups
# particles:
player_attack_particles = pygame.sprite.GroupSingle()

# player:
player_sprite = pygame.sprite.GroupSingle()
goal_sprite = pygame.sprite.GroupSingle()
player_constraint_sprites = pygame.sprite.Group()

# enemy
enemy_sprites = pygame.sprite.Group()
enemy_constraint_sprites = pygame.sprite.Group()

# level
terrain_sprites = pygame.sprite.Group()
cloud_sprites = pygame.sprite.Group()
stone_sprites = pygame.sprite.Group()
tree_sprites = pygame.sprite.Group()
mountain_sprites = pygame.sprite.Group()
npc_sprites = pygame.sprite.Group()

# buttons:
goal_button_sprite = pygame.sprite.GroupSingle()
