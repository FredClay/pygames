import pygame
from settings import BIRD_SPRITE


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = BIRD_SPRITE
        self.rect = self.image.get_rect(topleft=(40, 200))
        self.jump_speed = -4
        self.vert_vel = 0
        self.gravity = 0.25

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.vert_vel = 0
                    self.vert_vel += self.jump_speed

    def apply_gravity(self):
        self.vert_vel += self.gravity

    def update(self):
        self.get_input()
        self.apply_gravity()
