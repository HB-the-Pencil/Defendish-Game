import sys

import pygame
from pygame.locals import *

from settings import Settings

from ship import Ship


class Defendish:
    """Class to manage game assets, behavior, etc."""

    def __init__(self):
        """
        Initialize pygame and create the game resources.
        """
        pygame.init()

        self.settings = Settings()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h)
        )

        pygame.display.set_caption("Defendish")

        self.bg_color = (220, 220, 220)

        self.ship = Ship(self)

    def _check_events(self):
        """
        Check the pygame events and respond to them.

        :return: Performs various actions based on the event, e.g. quits the
            game when the QUIT event happens (alt + f4 or X button).
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self.ship.moving_r = True
                    # Eventually, this will change to "flip" the ship at the
                    # edge of the motion field (where it changes to the
                    # background scroll instead).
                    self.ship.dir = "r"

                elif event.key == K_LEFT:
                    self.ship.moving_l = True
                    self.ship.dir = "l"

                if event.key == K_UP:
                    self.ship.moving_u = True

                elif event.key == K_DOWN:
                    self.ship.moving_d = True

            elif event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.ship.moving_r = False

                elif event.key == K_LEFT:
                    self.ship.moving_l = False

                if event.key == K_UP:
                    self.ship.moving_u = False

                elif event.key == K_DOWN:
                    self.ship.moving_d = False

    def _update_screen(self):
        """
        Update the screen and call draw functions.

        :return: Draws images to the screen and flips the display.
        """
        # Redraw the background.
        self.screen.fill(self.settings.bg_color)

        # Draw and update the ship.
        self.ship.update()
        self.ship.draw()

        # Flip the display.
        pygame.display.flip()

    def run_game(self):
        """
        Start the main game loop.

        :return: Runs the entire game. If the user quits, close pygame safely.
        """
        while True:
            # Check the events.
            self._check_events()

            # Update the display.
            self._update_screen()

            # Run the program at a smooth framerate.
            self.clock.tick(60)


if __name__ == "__main__":
    # Create the game instance and run it.
    d_game = Defendish()
    d_game.run_game()