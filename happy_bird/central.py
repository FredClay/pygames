"""Flappy Bird clone."""
import pygame
from level import Level
from settings import *

WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Happy Bird")


def draw_window(level):
    """Updates the screen."""
    WIN.blit(BG_IMAGE, (0, 0))
    level.run_level()
    score_text = SCORE_FONT.render(f"Score: {int(level.score)}", True, WHITE)
    WIN.blit(score_text, (10, SCREEN_HEIGHT - 40))
    pygame.display.update()


def main():
    """Runs the game instance."""
    clock = pygame.time.Clock()

    level = Level(WIN)
    level.setup_bird()

    game_active = True
    while game_active:
        clock.tick(FPS)

        if not level.active_game:
            game_active = False
        draw_window(level)

    pygame.quit()


if __name__ == '__main__':
    main()
