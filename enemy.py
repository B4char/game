import pygame
from random import randint
from support import create_enemy_animation_list
from sprite_groups import enemy_constraint_sprites, terrain_sprites, player_sprite
from settings import gravity, enemy_max_health
from particles import AttackParticles


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, x, y, scale, display_surface, color):
        super().__init__(group)
        self.display_surface = display_surface  # screen
        self.scale = scale  # enemy scale

        # animation:
        self.animation_list = create_enemy_animation_list(scale, color)
        self.frame_index = 0  # current frame in the animation list
        self.action = 1  # 0 - idle, 1 - walk, 2 - fall, 3 - attack, 4 - death
        self.image = self.animation_list[self.action][self.frame_index]

        # rect and position:
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect.y -= 110 - self.image.get_size()[1]
        self.old_rect = self.rect.copy()
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # vision rect:
        # rectangle for the attack hitbox
        self.attack_hitbox = pygame.rect.Rect(self.pos.x, self.pos.y, self.rect.width, self.rect.height)
        # rectangle for the enemy's vision
        self.vision_rect = pygame.rect.Rect(self.pos.x, self.pos.y, 500, 50)

        # enemy variables:
        # movement
        self.falling_speed = 0  # falling speed
        self.speed = 2  # speed
        self.direction = 1  # which direction is the enemy facing ? (1 - right, -1 - left)
        self.flip = False  # where is the enemy facing ? (False - right, True - left)
        self.idle = False  # is the enemy idle ? (yes/no)

        # attack
        self.on_player = False  # can the enemy see the player ? (yes/no)
        self.attacking = False  # if the enemy is currently attacking (mid attack animation)
        self.hit = False  # if the enemy has already hit the player in the current attack - True, else - False
        self.idle_attack = False  # is the enemy idle after the attack ? (yes/no)

        # health / status
        self.is_alive = True  # is the player alive ? (yes/no)
        self.health = enemy_max_health  # enemy health

        # timers
        self.animation_timer = pygame.time.get_ticks()  # animation timer
        self.idle_timer = pygame.time.get_ticks()  # idle timer
        self.attack_timer = pygame.time.get_ticks()  # attack timer
        self.idle_attack_timer = pygame.time.get_ticks()  # idle after attack timer
        self.hit_timer = pygame.time.get_ticks()  # hit timer

        self.attack_particles_sprite = pygame.sprite.GroupSingle()  # a sprite group for the attack particles

    def animate(self):
        # the function animates the enemy

        # the enemy is idle
        if self.action == 0:
            animation_speed = 260
        # the enemy is walking
        elif self.action == 1:
            animation_speed = 150
        # the enemy is falling
        elif self.action == 2:
            animation_speed = 300
        # the enemy is attacking
        elif self.action == 3:
            animation_speed = 85
        # the enemy is dead
        else:
            animation_speed = 80
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        self.image = pygame.transform.flip(self.image, self.flip, False)
        if self.action == 4:
            if not self.flip:
                self.rect.x -= 24
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.animation_timer > animation_speed:
            self.animation_timer = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 4:
                self.frame_index = len(self.animation_list[self.action]) - 1
            elif self.action == 3:
                self.update_enemy_to_idle()
                self.frame_index = 0
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.animation_timer = pygame.time.get_ticks()

    def collision(self, direction):
        # check collision between sprites, returns a list of all sprites that intersect with another sprite:
        collision_sprites = pygame.sprite.Group()
        collision_sprites.add(terrain_sprites)
        collision_sprites = pygame.sprite.spritecollide(self, collision_sprites, False)
        # check if there are sprites inside the collision group:
        if collision_sprites:
            # check direction:
            if direction == 'horizontal':
                for sprite in collision_sprites:
                    # collision on the right:
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.x

                    # collision on the left:
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.x

            if direction == 'vertical':
                for sprite in collision_sprites:
                    # collision on the bottom:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.y
                        self.falling_speed = 0

                    # collision on the top:
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.y

    def move(self, shift_x):
        # update and check collision in the x direction:
        self.pos.x += self.speed + shift_x
        self.rect.x = round(self.pos.x)
        self.collision('horizontal')

        # update and check collision in the y direction:
        # gravity:
        self.falling_speed += gravity
        if self.falling_speed > 16:
            self.falling_speed = 16

        self.pos.y += self.falling_speed
        self.rect.y = round(self.pos.y)
        self.collision('vertical')

    def reverse(self):
        # flip the enemy
        self.speed *= -1
        self.direction *= -1
        self.flip = not self.flip
        if self.flip:
            self.pos.x -= 2
        else:
            self.pos.x += 2

    def check_alive(self):
        # checks if the enemy is alive
        if self.health <= 0:
            self.is_alive = False

    def check_reverse_collision(self):
        reverse_sprites = pygame.sprite.spritecollide(self, enemy_constraint_sprites, False)
        if reverse_sprites:
            for sprite in reverse_sprites:
                if self.flip:
                    if self.rect.left == sprite.rect.left:
                        self.reverse()
                else:
                    if self.rect.right == sprite.rect.right:
                        self.reverse()

    def random_movement(self):
        if not self.idle_attack:
            self.check_reverse_collision()  # check for reverse collision
            self.random_reverse()

            if pygame.time.get_ticks() - self.idle_timer > 5500:  # if the enemy was idle for the last 5.5 sec
                self.idle = False

            if not self.idle:  # the player isn't idle
                self.update_enemy_to_move()
                self.random_idle()

    def random_reverse(self):
        if randint(1, 1000) == 1:
            self.reverse()

    def random_idle(self):
        if randint(1, 1200) == 1 and not self.idle:  # the enemy isn't idling rn
            # idle the enemy
            self.update_enemy_to_idle()

    def chase_movement(self):
        self.face_player()
        if not self.idle_attack:
            self.idle = False
            if pygame.Rect.colliderect(self.attack_hitbox, player_sprite.sprite.hitbox):
                self.update_enemy_to_attack()

            if not self.attacking:
                self.update_enemy_to_move()

    def face_player(self):
        player = player_sprite.sprite
        if not self.flip:  # the enemy is facing right
            if self.pos.x > player.pos.x:
                self.flip = True
                self.direction = -1
                self.speed *= -1
        else:  # the enemy is facing left
            if self.pos.x < player.pos.x:
                self.flip = False
                self.direction = 1
                self.speed *= -1

    def check_vision_collision(self):
        if pygame.Rect.colliderect(self.vision_rect, player_sprite.sprite.rect):
            self.on_player = True
            self.idle = False
        else:
            self.on_player = False

    def update_enemy_to_idle(self):
        self.idle = True
        self.speed = 0
        self.update_action(0)
        self.idle_timer = pygame.time.get_ticks()

    def update_enemy_to_move(self):
        self.speed = 2 * self.direction
        self.update_action(1)

    def update_enemy_to_attack(self):
        self.attack_timer = pygame.time.get_ticks()
        self.idle_attack_timer = pygame.time.get_ticks()
        self.hit_timer = pygame.time.get_ticks()
        self.speed = 0
        self.update_action(3)
        self.attacking = True
        self.idle_attack = True
        AttackParticles(self.rect.topleft, self.scale, self.attack_particles_sprite)

    def check_attack_collision(self):
        player = player_sprite.sprite
        if pygame.Rect.colliderect(self.attack_hitbox, player.hitbox):
            # check if the enemy hasn't already hit the player
            if not self.hit and pygame.time.get_ticks() - self.hit_timer > 200:
                player.health -= randint(4, 9)
                self.hit = True
                print(player.health)

    def update_enemy_to_death(self):
        self.speed = 0
        self.update_action(4)

    def update_rectangles(self):
        # update rectangles:
        self.old_rect = self.rect.copy()  # update old_rectangle
        if self.flip:  # the enemy is facing left
            self.vision_rect.topright = (self.rect.right + 150, self.rect.top + 10)  # vision rect
            self.attack_hitbox.update(round(self.pos.x) - 30, round(self.pos.y),
                                      self.attack_hitbox.width, self.attack_hitbox.height)  # attack hitbox rect
        else:  # the enemy is facing right
            self.vision_rect.topleft = (self.rect.left - 150, self.rect.top + 10)  # vision rect
            self.attack_hitbox.update(round(self.pos.x) + 25, round(self.pos.y),
                                      self.attack_hitbox.width, self.attack_hitbox.height)  # attack hitbox rect

    def update_timers(self):
        if pygame.time.get_ticks() - self.attack_timer > 500:
            self.attacking = False
            self.hit = False
        else:
            self.check_attack_collision()

        if pygame.time.get_ticks() - self.idle_attack_timer > 1400:
            self.idle_attack = False

    def enable_hitbox(self):
        # enables hitbox for debug
        pygame.draw.rect(self.display_surface, 'green', self.vision_rect, 2)  # vision
        pygame.draw.rect(self.display_surface, 'red', self.attack_hitbox, 2)  # attack hitbox
        pygame.draw.rect(self.display_surface, 'black', self.rect, 2)  # rect
        pygame.draw.rect(self.display_surface, 'lightblue', self.old_rect, 2)  # old rect

    def update(self, shift_x):
        # self.enable_hitbox()
        self.check_alive()
        self.update_rectangles()

        # enemy movement:
        if self.is_alive:  # the enemy is alive
            self.update_timers()
            self.check_vision_collision()
            if player_sprite.sprite.is_alive:  # the player is alive
                if self.on_player:  # the enemy is on the player (chasing the player)
                    self.chase_movement()
                else:  # the enemy is not on the player (not chasing the player)
                    self.random_movement()
            else:  # the player is dead
                self.update_enemy_to_idle()
        else:  # the enemy is dead
            self.update_enemy_to_death()

        self.move(shift_x)

        # animation:
        self.animate()
        self.attack_particles_sprite.update(self.flip, self.pos, self.display_surface, not self.is_alive)
        self.attack_particles_sprite.draw(self.display_surface)
