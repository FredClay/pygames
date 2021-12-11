import pygame
import os
pygame.font.init()

# Initialisation Settings
FPS = 60
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 400

# Colours
GREY = (100, 100, 100)
RED = (200, 20, 20)
GREEN = (0, 200, 50)
WHITE = (255, 255, 255)

# Bird PNG
BIRD_SPRITE_IMAGE = pygame.image.load(os.path.join('Assets', 'bird.png'))
BIRD_SPRITE = pygame.transform.scale(BIRD_SPRITE_IMAGE, (26, 20))

# Tube PNGs
BOTTOM_TUBE_PNG = pygame.image.load(os.path.join('Assets', 'tube.png'))
BOTTOM_TUBE_FIN = pygame.transform.scale(BOTTOM_TUBE_PNG, (30, BOTTOM_TUBE_PNG.get_height()))
TOP_TUBE_FIN = pygame.transform.flip(BOTTOM_TUBE_FIN, False, True)

# Background PNG
BG_IMAGE = pygame.image.load(os.path.join('Assets', 'background.png'))

# Game settings
SCROLL_SPEED = -3
TUBE_DELAY = 70

# Fonts
SCORE_FONT = pygame.font.SysFont('Arial', 30)
