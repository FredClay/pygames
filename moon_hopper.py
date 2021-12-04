"""Python file for 'Moon Hopper'.
This is a basic 2D infinite-scroll game built with Pygame."""

# python3
# Installed libraries:
import pygame

# Python Standard libraries:
import os
import random
import sys

pygame.font.init()

# Initial Game Settings. Can be modified to impact gameplay.
SCREEN_WIDTH = 1080  # Should be between 720 and 1080. Smaller is harder.
SCREEN_HEIGHT = 200  # Do not edit due to limitations of BG_IMAGE.
SCREEN_MID_X = SCREEN_WIDTH // 2
SCREEN_MID_Y = SCREEN_HEIGHT // 2

BORDER_HEIGHT = SCREEN_HEIGHT * 0.1
BORDER = pygame.Rect(0, SCREEN_HEIGHT - BORDER_HEIGHT, SCREEN_WIDTH, BORDER_HEIGHT)

# COLOURS
BG_COLOUR = (100, 200, 150)
SPACE_COLOUR = (20, 20, 100)
YELLOW = (255, 255, 0)
SOFT_YELLOW = (180, 180, 100)
WHITE = (255, 255, 255)

# Game specs
FPS = 60
ROLL_SPEED = 5
MAX_SPIKES = 10
SPIKE_WIDTH = 15
SPIKE_HEIGHT = 20
SPIKE_SPAWN_FREQ = 5  # Enter integer as percentage of 100. e.g. 5 = 0.05% chance of spawn. Recommended: 5
SPIKE_BREAK = 3

# Player Specs
PLAYER_WIDTH = 55
PLAYER_HEIGHT = 40
PLAYER_LIVES = 3
PLAYER_X_VEL = 4
PLAYER_FALL_SPEED = 0.2

# Scoring Specs
SCORE_FONT = pygame.font.SysFont('Arial', 20)
FINAL_SCORE_FONT = pygame.font.SysFont('Arial', 60)

# Events
PLAYER_HIT = pygame.USEREVENT + 1
SCORED = pygame.USEREVENT + 2

# Building window for game...
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moon Hopper")

# Background image. Loaded from 'Assets' folder. Assets should be in same directory as 'moon_hopper.py'.
BG_IMAGE = pygame.image.load(os.path.join('Assets', 'Space_Game_BG.png'))

# Sprites stored in an 'Assets' folder. Assets should be in same directory as 'moon_hopper.py'.
PLAYER_SPRITE_IMAGE = pygame.image.load(os.path.join('Assets', 'player_grounded.png'))
PLAYER_JUMP_IMAGE = pygame.image.load(os.path.join('Assets', 'player_jumping.png'))

PLAYER_SPRITE = pygame.transform.scale(PLAYER_SPRITE_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))
PLAYER_JUMP_SPRITE = pygame.transform.scale(PLAYER_JUMP_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))

SPIKE_IMAGE = pygame.image.load(os.path.join('Assets', 'spike.png'))


def draw_window(player, spikes, player_score, sprite_for_player):
    """Updates the screen for every frame of the game run cycle."""
    WIN.blit(BG_IMAGE, (0, 0))
    player_score_text = SCORE_FONT.render("SCORE:" + str(player_score), True, WHITE)
    WIN.blit(player_score_text, (SCREEN_WIDTH - 200, 20))
    pygame.draw.rect(WIN, SOFT_YELLOW, BORDER)
    WIN.blit(sprite_for_player, (player.x, player.y))
    for spike in spikes:
        this_spike_image = pygame.transform.scale(SPIKE_IMAGE, (spike.width, spike.height))
        WIN.blit(this_spike_image, (spike.x, spike.y))
    pygame.display.update()


def draw_final_score(player_score):
    """Upon the player's death, their score is displayed."""
    final_score_text = FINAL_SCORE_FONT.render("FINAL SCORE: " + str(player_score), True, WHITE)
    WIN.blit(final_score_text, (10, 10))
    pygame.display.update()
    pygame.time.delay(5000)


def handle_player_position(keys_pressed, player, player_vert_vel, player_vert_catcher):
    """Converts user input to on-screen movement of player sprite."""
    player_direction = 'RIGHT'
    if keys_pressed[pygame.K_UP] and player_vert_vel == 0:
        player_vert_catcher = player.y
        player_vert_vel = 5
    if keys_pressed[pygame.K_LEFT] and player.x - PLAYER_X_VEL > 0:
        player.x -= PLAYER_X_VEL
        player_direction = 'LEFT'
    if keys_pressed[pygame.K_RIGHT] and player.x + player.width + PLAYER_X_VEL < SCREEN_WIDTH:
        player.x += PLAYER_X_VEL
    if player_vert_vel:
        player.y -= player_vert_vel
        player_vert_vel -= PLAYER_FALL_SPEED
        if player_vert_catcher <= player.y:
            player_vert_vel = 0

    return player_vert_vel, player_direction


def manage_spikes(spikes, player):
    """Manages the movement of spikes from left to right. Also checks for player-spike
    collisions and deletes any redundant spikes."""
    for spike in spikes:
        spike.x -= ROLL_SPEED
        if spike.x + SPIKE_WIDTH < 0:
            spikes.remove(spike)
            pygame.event.post(pygame.event.Event(SCORED))
        if player.colliderect(spike):
            pygame.event.post(pygame.event.Event(PLAYER_HIT))


def player_sprite(player_vert_vel, player_direction):
    """Determines which of the player sprites to display."""
    sprite = PLAYER_SPRITE
    if player_vert_vel != 0:
        sprite = PLAYER_JUMP_SPRITE
    if player_direction == 'LEFT':
        sprite = pygame.transform.flip(sprite, True, False)
    return sprite


def main():
    """Boots up the window and runs the game based upon certain conditions."""
    if not 720 <= SCREEN_WIDTH <= 1080 or SCREEN_HEIGHT != 200:
        print("Specified screen dimensions not valid.\n"
              "Max width is: 1080. Min width is 720.\nHeight MUST be 200.", file=sys.stderr)
        sys.exit()

    player = pygame.Rect(50, SCREEN_HEIGHT - PLAYER_HEIGHT - BORDER_HEIGHT, PLAYER_WIDTH - 20, PLAYER_HEIGHT - 10)
    clock = pygame.time.Clock()

    player_score = 0

    player_vert_vel = 0
    player_vert_catcher = player.y

    time_since_spike = FPS

    spikes = []

    game_active = True
    while game_active:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False

            if event.type == PLAYER_HIT:
                game_active = False
                draw_final_score(player_score)

            if event.type == SCORED:
                player_score += 1

        if time_since_spike > SPIKE_BREAK and len(spikes) < MAX_SPIKES:
            random_spawn = random.randint(1, 100)
            if random_spawn < SPIKE_SPAWN_FREQ:
                if random_spawn < 3:
                    random_spawn += 2
                spike_height = random_spawn * 12
                spike_width = random_spawn * 5
                spike = pygame.Rect(SCREEN_WIDTH - spike_width, SCREEN_HEIGHT - spike_height - BORDER_HEIGHT,
                                    spike_width, spike_height)
                spikes.append(spike)
                time_since_spike = 0
        time_since_spike += 1

        manage_spikes(spikes, player)
        keys_pressed = pygame.key.get_pressed()
        player_vert_vel, player_direction = handle_player_position(keys_pressed, player,
                                                                   player_vert_vel, player_vert_catcher)

        players_sprite = player_sprite(player_vert_vel, player_direction)
        draw_window(player, spikes, player_score, players_sprite)

    print("Game Over!")
    print(f"Final score was: {player_score}")
    pygame.quit()


if __name__ == '__main__':
    main()
