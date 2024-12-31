import sys
import random as r

import pygame
from pygame.locals import *

from settings import Settings

from ship import Ship
from lazer import Lazer
from star import Star

class Defendish:
    """Class to manage game assets, behavior, etc."""

    def __init__(self):
        """
        Initialize pygame and create the game resources.
        """
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("Monospace", 18, bold=True)

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
        self.lazers = pygame.sprite.Group()
        self.reload = 0

        # Sound things. Sounds from woolyss.com.
        self.fly_sound = pygame.mixer.Sound("sounds/Defender_Thrust.wav")
        self.lazer_sound = pygame.mixer.Sound("sounds/Defender_Fire.wav")

        self.channel_ship = pygame.mixer.Channel(0)
        self.channel_lazer = pygame.mixer.Channel(1)

        self.cam = self.ship.cam

        self.stars = [
            Star(r.randint(0, self.bg_w // self.settings.parallax),
                r.randint(32 * self.scale, 180 * self.scale), self
            ) for i in range(10)
        ]


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
            if not self.channel_ship.get_busy():
                self.channel_ship.play(self.fly_sound)

        if event.key == K_LEFT:
            self.ship.moving_l = True
            if not self.channel_ship.get_busy():
                self.channel_ship.play(self.fly_sound)

        if event.key == K_SPACE:
            self._shoot_lazer()

        if event.key == K_q:
            pygame.quit()
            sys.exit()


    def _check_keyup_events(self, event):
        """
        Process events when a key is up.

        :param event: Keypress event that was triggered.
        :return: Stops moving the ship, etc.
        """
        if event.key == K_RIGHT:
            self.channel_ship.stop()
            self.ship.moving_r = False

        if event.key == K_LEFT:
            self.channel_ship.stop()
            self.ship.moving_l = False

        if event.key == K_UP:
            self.ship.moving_u = False

        elif event.key == K_DOWN:
            self.ship.moving_d = False

    def _shoot_lazer(self):
        """
        Fire a lazer.

        :return: Adds a lazer to the lazer group.
        """
        if len(self.lazers) < self.settings.fire_limit and self.reload <= 0:
            self.channel_lazer.play(self.lazer_sound)
            new_lazer = Lazer(self)
            self.lazers.add(new_lazer)
            self.reload = self.settings.reload

        self.reload -= 1

    def _update_screen(self):
        """
        Update the screen and call draw functions.

        :return: Draws images to the screen and flips the display.
        """
        self._draw_bg()

        # Draw the bullets.
        for lazer in self.lazers.sprites():
            lazer.draw()

        # Draw the ship.
        self.ship.draw()

        # This is where the scanner will go.
        self._draw_scanner()

        # Debug stats.
        if self.settings.debug:
            c_pos = self.font.render(
                f"Cam:({int(self.cam.x)}, {int(self.cam.y)})",
                True, (0, 0, 255)
            )
            p_pos = self.font.render(
                f"P1:({int(self.ship.x)}, {int(self.ship.y)})",
                True, (0, 0, 255)
            )
            self.screen.blit(c_pos, (236 * self.scale, 4 * self.scale))
            self.screen.blit(p_pos, (236 * self.scale, 16 * self.scale))

        # Update the display.
        pygame.display.update()

    def _draw_bg(self):
        """
        Draw the background.

        :return: Draws a looping background to the screen.
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

        # Draw the stars.
        for star in self.stars:
            star.update()
            star.draw()


    def _draw_scanner(self):
        """
        Draw the landscape scanner.

        :return: Draws the scanner to the screen.
        """
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


    def run_game(self):
        """
        Start the main game loop.

        :return: Runs the entire game. If the user quits, close pygame safely.
        """
        while True:
            # Check the events.
            self._check_events()

            # Update ship and bullets.
            self.ship.update()
            self.lazers.update()

            # Update the display.
            self._update_screen()

            # Run the program at a smooth framerate.
            self.clock.tick(60)