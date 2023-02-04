import pygame
from random import randint
from support import create_enemy_animation_list
from sprite_groups import enemy_constraint_sprites, terrain_sprites, player_sprite, enemy_attack_particles
from settings import gravity
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
        self.vision_rect = pygame.rect.Rect(self.pos.x, self.pos.y, 350, 50)

        # enemy variables:
        # movement
        self.falling_speed = 0  # falling speed
        self.speed = 2  # speed
        self.direction = 1  # which direction is the enemy facing ? (1 - right, -1 - left)
        self.idling_cooldown = 0  # cooldown for the idling animation
        self.flip = False  # where is the enemy facing ? (False - right, True - left)
        self.idling = False  # is the enemy idling ? (yes/no)

        # attack
        self.hit = False
        self.hitting = False  # is the enemy at the middle of the attack animation ? (yes/no)
        self.on_player = False  # can the enemy see the player ? (yes/no)
        self.idling_after_attack = False  # the enemy is idling ? (yes/no)
        self.idling_after_attack_cooldown = 0  # cooldown for the idling animation
        self.attack_cooldown = 0  # attack cooldown for the next attack

        # health / status
        self.is_alive = True  # is the player alive ? (yes/no)
        self.health = 150  # enemy health

        # timers
        self.update_kill_time = pygame.time.get_ticks()  # death animation
        self.update_time = pygame.time.get_ticks()  # animations

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
        if pygame.time.get_ticks() - self.update_time > animation_speed:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:  # 3 - attacking
                self.idle_after_attack()
                self.attack_cooldown = 50
                self.hit = False
            elif self.action == 4:  # 4 - death
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

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

    def ai_random_movement(self):
        # a function for a random movement
        if self.idling_cooldown == 0:
            self.idling = False
            self.speed = 2 * self.direction
            self.update_action(1)  # 1 - walking
            self.idle()
            self.random_reverse()

    def idle_after_attack(self):
        # the function idles the enemy
        self.idling_after_attack_cooldown = 75
        self.idling_after_attack = True
        self.update_action(0)  # 0 - idle

    def ai_after_player_movement(self):
        # a function for the movement when the enemy is chasing a player
        if not self.hitting:
            self.speed = 3 * self.direction
        player = player_sprite.sprite
        # face the player:
        if self.pos.x < player.pos.x:
            if self.direction == -1:
                self.reverse()
        elif self.pos.x > player.pos.x:
            if self.direction == 1:
                self.reverse()

        # check if the enemy can attack
        if self.attack_cooldown == 0:
            # check if the player is in range to attack:
            if self.attack_hitbox.colliderect(player.rect):  # the player is in range
                self.attack()
            else:
                self.update_action(1)

    def attack(self):
        # an attack function which makes the enemy attack the player
        self.update_action(3)  # 3 - attacking
        AttackParticles(self.rect.topleft, self.scale, enemy_attack_particles)  # create attack particles
        self.attack_cooldown = 50  # set attack cooldown to 200
        self.speed = 0

    def random_reverse(self):
        # a function that makes the enemy reverse
        if randint(1, 1200) == 1:
            self.reverse()

    def idle(self):
        # a function that makes the enemy idle
        if randint(1, 400) == 1:
            self.update_action(0)  # 0 - idle
            self.idling = True
            self.speed = 0
            self.idling_cooldown = randint(150, 400)

    def reverse(self):
        # flip the enemy
        self.speed *= -1
        self.direction *= -1
        self.flip = not self.flip
        if self.flip:
            self.pos.x -= 2
        else:
            self.pos.x += 2

    def kill_enemy(self):
        # a function to kill the enemy
        if pygame.time.get_ticks() - self.update_kill_time > 120:
            self.update_action(4)  # 4 - death

    def check_alive(self):
        # checks if the enemy is alive
        if self.health <= 0:
            self.is_alive = False

    def check_vision(self):
        # check if the player is inside the enemy vision rect (the enemy can see the player)
        if self.vision_rect.colliderect(player_sprite.sprite.rect):
            self.on_player = True
        else:
            self.on_player = False

    def hit_collision(self):
        player = player_sprite.sprite
        if self.hitting:
            if pygame.Rect.colliderect(self.attack_hitbox, player.rect) and player.is_alive:
                if not self.hit:
                    player.health -= 1
                    self.hit = True

    def update(self, shift_x):
        pygame.draw.rect(self.display_surface, 'black', self.vision_rect, 2)  # vision
        # pygame.draw.rect(self.display_surface, 'green', self.attack_hitbox, 2)  # hitbox
        pygame.draw.rect(self.display_surface, 'red', self.rect, 2)  # self.rect
        self.check_alive()

        # idling counter:
        if self.idling_cooldown > 0:
            self.idling_cooldown -= 1
        # attack cooldown:
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        # attack idle cooldown:
        if self.idling_after_attack_cooldown > 0:
            self.idling_after_attack_cooldown -= 1
        if self.idling_after_attack_cooldown == 0:
            self.idling_after_attack = False

        # attack particles:
        if self.action == 3:
            self.hitting = True
        else:
            self.hitting = False

        if self.hitting:
            enemy_attack_particles.update(self.flip, self.pos, self.display_surface)
            enemy_attack_particles.draw(self.display_surface)

        # update rectangles:
        self.old_rect = self.rect.copy()  # update old_rectangle
        if self.flip:  # the enemy is facing left
            self.vision_rect.topright = (self.rect.right + 50, self.rect.top + 10)  # vision rect
            self.attack_hitbox.update(round(self.pos.x) - 30, round(self.pos.y),
                                      self.attack_hitbox.width, self.attack_hitbox.height)  # attack hitbox rect
        else:  # the enemy is facing right
            self.vision_rect.topleft = (self.rect.left - 50, self.rect.top + 10)  # vision rect
            self.attack_hitbox.update(round(self.pos.x) + 25, round(self.pos.y),
                                      self.attack_hitbox.width, self.attack_hitbox.height)  # attack hitbox rect

        # enemy movement:
        self.check_vision()
        # check if the player is alive:
        if self.is_alive:  # the enemy is alive
            self.update_kill_time = pygame.time.get_ticks()  # update check kill time
            # check if the enemy can see the player:
            if not self.on_player:  # the enemy can't see the player
                # check if the enemy is in idle action
                if not self.idling_after_attack:  # the enemy isn't idling
                    self.ai_random_movement()
                # check if the enemy is colliding with a reverse object:
                if pygame.sprite.spritecollide(self, enemy_constraint_sprites, False):
                    for reverse_sprite in enemy_constraint_sprites.sprites():
                        if self.flip:
                            if self.rect.left == reverse_sprite.rect.left:
                                self.reverse()
                        else:
                            if self.rect.right == reverse_sprite.rect.right:
                                self.reverse()

            else:  # the enemy can see the player
                # check if the enemy is idling after his attack:
                if not self.idling_after_attack:  # the enemy isn't idling
                    self.ai_after_player_movement()

        else:  # the enemy is dead
            self.speed = 0
            self.kill_enemy()

        self.move(shift_x)
        self.hit_collision()

        # animation:
        self.animate()
