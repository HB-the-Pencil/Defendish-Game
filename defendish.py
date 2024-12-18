import sys
import subprocess

try:
    subprocess.check_call([sys.executable,
        "-m", "pip", "install", "-r", "requirements.txt"])
except subprocess.CalledProcessError:
    print("Error importing modules")

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

        self.scale = self.settings.scale

        pygame.display.set_caption("Defendish")

        self.bg = pygame.image.load("images/bg.png")
        self.bg = pygame.transform.scale(self.bg,
            (self.bg.get_width() * self.scale,
             self.bg.get_height() * self.scale)
        )
        self.bg_rect = self.bg.get_rect()

        self.bg_rect.x = 0
        self.bg_rect.y = 32 * self.scale

        self.bg_w = self.bg_rect.w

        self.ship = Ship(self)

        self.cam = self.ship.cam


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
                self._check_keydown_events(event)

            elif event.type == KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        """
        Process events when a key is down.

        :param event: Keypress event that was triggered.
        :return: Moves the ship, fires bullets, etc.
        """
        if event.key == K_UP:
            self.ship.moving_u = True

        elif event.key == K_DOWN:
            self.ship.moving_d = True

        if event.key == K_RIGHT:
            self.ship.moving_r = True

        if event.key == K_LEFT:
            self.ship.moving_l = True

        elif event.key == K_q:
            pygame.quit()
            sys.exit()


    def _check_keyup_events(self, event):
        """
        Process events when a key is up.

        :param event: Keypress event that was triggered.
        :return: Stops moving the ship, etc.
        """
        if event.key == K_RIGHT:
            self.ship.moving_r = False

        if event.key == K_LEFT:
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

        # Loop the camera.
        if self.cam.x < -self.bg_w:
            self.cam.x = self.bg_w

        if self.cam.x > self.bg_w:
            self.cam.x = -self.bg_w

        self.bg_rect.x = self.cam.x
        self.screen.blit(self.bg, self.bg_rect)

        # These extra draws are to provide the illusion of a loop.
        self.bg_rect.x = self.cam.x + self.bg_w
        self.screen.blit(self.bg, self.bg_rect)

        self.bg_rect.x = self.cam.x - self.bg_w
        self.screen.blit(self.bg, self.bg_rect)

        # Draw and update the ship.
        self.ship.update()
        self.ship.draw()

        # This is where the scanner will go.

        # Draw the map.
        pygame.draw.rect(self.screen, (0, 0, 0),
            (60 * self.scale, 0, 172 * self.scale, 32 * self.scale)
        )
        pygame.draw.line(self.screen, (255, 0, 0),
            (60 * self.scale, 26 * self.scale),
            (232 * self.scale, 26 * self.scale), self.scale
        )

        # Draw the player's ship.
        pygame.draw.rect(self.screen, (255, 255, 255),
            (60 * self.scale - (self.cam.x - self.bg_w) / self.scale / 4,
             (self.ship.y - 32 * self.scale) / 6.5, self.scale, self.scale)
        )

        # Draw the borders.
        pygame.draw.line(self.screen, (0, 0, 255),
            (60 * self.scale, 0), (60 * self.scale, 32 * self.scale),
            self.scale
        )
        pygame.draw.line(self.screen, (0, 0, 255),
            (232 * self.scale, 0), (232 * self.scale, 32 * self.scale),
            self.scale
        )
        pygame.draw.line(self.screen, (0, 0, 255),
            (self.scale, 32 * self.scale),
            (291 * self.scale, 32 * self.scale), self.scale
        )

        # Update the display.
        pygame.display.update()


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