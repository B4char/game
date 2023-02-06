import pygame
from support import create_player_animation_list
from sprite_groups import terrain_sprites, player_attack_particles, enemy_sprites
from settings import screen_width, player_health, player_max_health, gravity, permanent_speed
from particles import AttackParticles


class Player(pygame.sprite.Sprite):
    def __init__(self, surface, pos, group, obstacles):
        super().__init__(group)
        # image:
        self.surface_display = surface
        self.scale = 2.5

        # player hp
        self.is_alive = True
        self.health = player_health
        self.max_health = player_max_health
        self.update_kill_time = pygame.time.get_ticks()

        # attack
        self.attacking = False
        self.attack_cooldown = 0

        # animation:
        self.flip = False
        self.update_time = pygame.time.get_ticks()
        self.attack_timer_damage = pygame.time.get_ticks()
        self.animation_list = create_player_animation_list(self.scale)
        self.action = 0  # 0 - idle, 1 - run, 2 - jump, 3 - fall, 4 - attack
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.rect.Rect(pos[0] + 10, pos[1], 30, self.rect.height)
        self.old_rect = self.rect.copy()

        # hitbox
        self.attack_hitbox = pygame.rect.Rect(pos[0], pos[1], self.rect.width * 1.2, 55)
        self.hit = False

        # movement:
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2()
        self.speed = permanent_speed
        self.jump_speed = 0
        self.obstacles = obstacles
        self.jump = False
        self.jump_event = False
        self.double_jump = 2

        # movement status:
        self.on_ground = False
        self.falling = False

    def animate(self):
        # the player is idling or jumping
        if self.action == 0 or self.action == 2:
            animation_speed = 260
        # the player is running
        elif self.action == 1:
            animation_speed = 150
        # the player is falling
        elif self.action == 3:
            animation_speed = 250
        # the player is attacking
        elif self.action == 4:
            animation_speed = 85
        else:  # the player is dead
            animation_speed = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        self.image = pygame.transform.flip(self.image, self.flip, False)
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_speed:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.action == 3:  # falling
            if self.frame_index > 1:
                self.frame_index = 0
        else:  # the player isn't falling
            if self.action == 4 and self.frame_index > 5:
                self.attacking = False
            # if the animation has run out then reset back to the start
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 2:  # 2 - jumping, 5 - death
                    self.frame_index = len(self.animation_list[self.action]) - 1
                elif self.action == 4:  # 4 - attacking
                    self.action = 0
                    self.frame_index = 0
                    self.hit = False
                else:
                    self.frame_index = 0

    def update_action(self):
        new_action = self.get_new_action()
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.update_time = pygame.time.get_ticks()
            self.frame_index = 0

    def get_new_action(self):
        if self.action == 4:
            new_action = 4
        # check if the player on ground
        elif self.on_ground:
            # check if the player is moving
            if self.direction.x != 0:
                new_action = 1
            # the player isn't moving
            else:
                new_action = 0
        # check if the player isn't on ground
        elif not self.on_ground:
            # check if the player is falling
            if self.falling:
                new_action = 3
            # the player is jumping
            else:
                new_action = 2
        # the player is doing nothing
        else:
            new_action = 0

        return new_action

    def attack(self):
        self.attack_timer_damage = pygame.time.get_ticks()
        AttackParticles(self.rect.topleft, self.scale, player_attack_particles)
        self.action = 4
        self.attacking = True
        self.frame_index = 0
        self.attack_cooldown = 100
        # attack !

    def input(self):
        keys = pygame.key.get_pressed()

        # movement input:
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.flip = True
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.flip = False
        else:
            self.direction.x = 0

        if self.jump_event and (self.on_ground or self.double_jump > 0):
            self.double_jump -= 1
            self.direction.y = -1
            self.jump_speed = 0
            self.jump = True
        else:
            self.direction.y = 0

    def collision(self, direction):
        # check for collision between sprites, returns a list of all sprites that intersect with another sprite
        collision_sprites = pygame.sprite.Group()
        collision_sprites.add(terrain_sprites)
        collision_sprites = pygame.sprite.spritecollide(self, collision_sprites, False)
        # check if there are sprites inside the obstacle group:
        if collision_sprites:
            # check direction:
            if direction == 'horizontal':
                for sprite in collision_sprites:
                    # collision on the right:
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.x

                    # collision on the left:
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.left:
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.x

            if direction == 'vertical':
                for sprite in collision_sprites:
                    # collision on the bottom:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.y
                        self.on_ground = True
                        self.jump_speed = 0
                        self.double_jump = 2

                    # collision on the top:
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.y
                        self.jump_speed = 0

    def hit_collision(self):
        if self.attacking:
            for enemy in enemy_sprites.sprites():
                if pygame.Rect.colliderect(self.attack_hitbox, enemy.rect) and enemy.is_alive:
                    if not self.hit:
                        if pygame.time.get_ticks() - self.attack_timer_damage > 380:
                            enemy.health -= 200
                            self.hit = True

    def move(self):
        # update and check collision in the x direction:
        self.pos.x += self.direction.x * self.speed
        self.rect.x = round(self.pos.x)
        self.collision('horizontal')
        # update and check collision in the y direction:
        # jump:
        if self.jump:
            self.jump_speed = -12
            self.jump = False
            self.on_ground = False
        # gravity:
        self.jump_speed += gravity
        if self.jump_speed > 18:
            self.jump_speed = 18

        if self.jump_speed > 1:
            self.on_ground = False
            self.falling = True
        else:
            self.falling = False

        self.pos.y += self.jump_speed
        self.rect.y = round(self.pos.y)
        self.collision('vertical')

    def inside_level(self):
        if self.rect.left <= 0:
            self.rect.left = 0
            self.pos.x = self.rect.x
        if self.rect.right >= screen_width:
            self.rect.right = screen_width
            self.pos.x = self.rect.x
        if self.rect.top <= 0:
            self.jump_speed = 0
            self.rect.top = 0
            self.pos.y = self.rect.y

    def check_alive(self):
        if self.health <= 0:
            self.is_alive = False

    def update_rectangles(self):
        # update rectangles:
        self.old_rect = self.rect.copy()
        if self.flip:
            self.hitbox.update(self.pos.x + 6, self.pos.y, self.hitbox.width, self.hitbox.height)
            self.attack_hitbox.update(round(self.pos.x) - 30, round(self.pos.y) + 10,
                                      self.attack_hitbox.width, self.attack_hitbox.height)
        else:
            self.hitbox.update(self.pos.x + 8, self.pos.y, self.hitbox.width, self.hitbox.height)
            self.attack_hitbox.update(round(self.pos.x) + 20, round(self.pos.y) + 10,
                                      self.attack_hitbox.width, self.attack_hitbox.height)

    def update(self, jump_event, attack_event):
        # pygame.draw.rect(self.surface_display, 'red', self.hitbox, 2)
        self.jump_event = jump_event
        self.check_alive()

        # update player position:
        self.inside_level()
        self.update_rectangles()
        # attack:
        if attack_event and self.attack_cooldown == 0 and self.jump_speed == 0:
            self.attack()
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        self.hit_collision()

        self.input()
        self.move()

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # animate the player
        player_attack_particles.update(self.flip, self.pos, self.surface_display, not self.is_alive)
        player_attack_particles.draw(self.surface_display)
        self.animate()
        self.update_action()
