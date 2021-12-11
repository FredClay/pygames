import pygame
from bird import Bird
from tubes import TopTube
from settings import SCREEN_HEIGHT, TUBE_DELAY


class Level:
    def __init__(self, display_surface):
        self.surface_to_draw_to = display_surface
        self.bird = pygame.sprite.GroupSingle()
        self.tubes = pygame.sprite.Group()
        self.active_game = True
        self.tube_time = 0
        self.tube_delay = TUBE_DELAY
        self.score = 0

    def setup_bird(self):
        self.bird.add(Bird())
        new_tube = TopTube()
        self.tubes.add(new_tube)
        self.tubes.add(new_tube.counterpart)

    def tube_adder(self):
        if self.tube_time == self.tube_delay:
            new_tube = TopTube()
            self.tubes.add(new_tube)
            self.tubes.add(new_tube.counterpart)
            self.tube_time = -1
        self.tube_time += 1

    def tube_manager(self):
        for tube in self.tubes.sprites()[0:2]:
            if tube.rect.right < -10:
                self.tubes.remove(tube)
                self.score += 0.5
            if tube.rect.colliderect(self.bird.sprite.rect):
                self.active_game = False

    def move_bird_vert(self):
        bird = self.bird.sprite
        bird.rect.y += bird.vert_vel
        if bird.rect.y > SCREEN_HEIGHT:
            self.active_game = False

    def run_level(self):
        self.bird.update()
        self.move_bird_vert()
        self.tube_adder()
        self.tubes.update()
        self.tube_manager()

        self.tubes.draw(self.surface_to_draw_to)
        self.bird.draw(self.surface_to_draw_to)
