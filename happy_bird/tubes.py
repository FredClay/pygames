import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SCROLL_SPEED
from settings import TOP_TUBE_FIN, BOTTOM_TUBE_FIN


class TopTube(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.top_tube_break = random.randint(50, SCREEN_HEIGHT - 150)
        self.image = TOP_TUBE_FIN
        self.rect = self.image.get_rect(bottomleft=(SCREEN_WIDTH, self.top_tube_break))
        self.counterpart = BottomTube(self.top_tube_break)

    def update(self):
        self.rect.x += SCROLL_SPEED
        self.counterpart.rect.x += SCROLL_SPEED


class BottomTube(pygame.sprite.Sprite):
    def __init__(self, counterpart_break):
        super().__init__()
        self.bottom_tube_break = counterpart_break + 80
        self.image = BOTTOM_TUBE_FIN
        self.rect = self.image.get_rect(topleft=(SCREEN_WIDTH, self.bottom_tube_break))
