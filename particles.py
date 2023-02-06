import pygame
from support import create_attack_particles


class AttackParticles(pygame.sprite.Sprite):
    def __init__(self, pos, scale, group):
        super().__init__(group)
        self.particles_list = create_attack_particles(scale)
        self.frame_index = 0
        self.image = self.particles_list[self.frame_index]
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - 4*scale))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.flip = False
        self.update_time = pygame.time.get_ticks()
        self.scale = scale

    def animate(self):
        animation_speed = 85
        self.image = self.particles_list[self.frame_index]
        self.image = pygame.transform.flip(self.image, self.flip, False)
        if self.flip:
            self.rect.update(self.pos[0] - self.scale * 10, self.pos[1], self.rect.width, self.rect.height)
        else:
            self.rect.update(self.pos[0], self.pos[1], self.rect.width, self.rect.height)
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_speed:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out then reset back to the start
        if self.frame_index >= len(self.particles_list):
            self.kill()

    def update(self, flip, pos, screen, kill):
        if kill:
            self.kill()
        self.pos = pos
        self.animate()
        self.flip = flip
