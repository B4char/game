import pygame

# setup sprite groups
# particles:
player_attack_particles = pygame.sprite.GroupSingle()
particles_sprite = pygame.sprite.Group()

# player:
player_sprite = pygame.sprite.GroupSingle()
goal_sprite = pygame.sprite.GroupSingle()
player_borders_sprites = pygame.sprite.Group()
health_orbs_sprites = pygame.sprite.Group()

# enemy
enemy_sprites = pygame.sprite.Group()
enemy_borders_sprites = pygame.sprite.Group()

# level
terrain_sprites = pygame.sprite.Group()
cloud_sprites = pygame.sprite.Group()
stone_sprites = pygame.sprite.Group()
tree_sprites = pygame.sprite.Group()
mountain_sprites = pygame.sprite.Group()
npc_sprite = pygame.sprite.GroupSingle()
bubble_text_sprite = pygame.sprite.GroupSingle()

# menu
menu_sprites = pygame.sprite.GroupSingle()
button_sprites = pygame.sprite.Group()

# buttons:
goal_button_sprite = pygame.sprite.GroupSingle()
npc_button_sprite = pygame.sprite.GroupSingle()
