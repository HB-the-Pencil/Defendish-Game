import pygame
from pygame.sprite import Sprite

import colorsys
import random

class Lazer(Sprite):
    """A class to create lazers."""

    def __init__(self, d_game):
        """
        Initialize a bullet at the ship's current position.

        :param d_game: The game that is currently running.
        """
        super().__init__()
        self.screen = d_game.screen
        self.settings = d_game.settings
        self.scale = self.settings.scale

        self.cam = d_game.cam
        self.ship = d_game.ship

        self.color = (255, 255, 255)
        self.trail = colorsys.hsv_to_rgb(pygame.time.get_ticks() % 360 / 360,
            1, 1
        )

        # Convert the trail color to integers.
        self.trail = (int(self.trail[0] * 255), int(self.trail[1] * 255),
            int(self.trail[2] * 255)
        )

        self.rect = pygame.Rect(0, 0, self.settings.lazer_width,
            self.settings.lazer_height
        )

        if self.ship.dir == "r":
            self.dir = "r"
            self.rect.x = self.ship.rect.x - self.rect.w
            self.rect.y = (self.ship.rect.y + self.ship.rect.h / 2
                           + self.scale)

        elif self.ship.dir == "l":
            self.dir = "l"
            self.rect.x = self.ship.rect.x + self.ship.rect.w
            self.rect.y = (self.ship.rect.y + self.ship.rect.h / 2
                           + self.scale)

        self.x = self.rect.x
        self.y = self.rect.y

        self.w = self.rect.w
        self.h = self.rect.h

        self.trail_rect = pygame.Rect(0, 0, 0, self.settings.lazer_height)

        self.speed = self.settings.lazer_speed

    def update(self):
        """
        Move the lazer on the screen.

        :return: Moves the bullet to the left or right, destroying it if it
            goes off-screen.
        """
        if self.dir == "r":
            self.x += self.speed

        elif self.dir == "l":
            self.x -= self.speed

        self.rect.x = self.x

        if (self.trail_rect.x + self.trail_rect.w < 0 or
                self.trail_rect.x > 292 * self.scale):
            self.kill()

        # Increase the size of the lazer trail and update the color.
        if self.dir == "r":
            self.trail_rect.midright = self.rect.midleft

        elif self.dir == "l":
            self.trail_rect.midleft = self.rect.midright

        if self.trail_rect.w < 15 * self.scale:
            self.trail_rect.w += self.speed / 6

        self.trail = colorsys.hsv_to_rgb(pygame.time.get_ticks() % 360 / 360,
            1, 1
        )

        # Convert the trail color to integers.
        self.trail = (int(self.trail[0] * 255), int(self.trail[1] * 255),
            int(self.trail[2] * 255)
        )

    def draw(self):
        """
        Draw the lazer to the screen.

        :return: Draws the lazer with a colorful trail.
        """
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, self.trail, self.trail_rect)

        if self.dir == "r" and self.trail_rect.w >= 10 * self.scale:
            for i in range(25):
                if random.randint(0, i) < 5:
                    pygame.draw.rect(self.screen, self.trail,
                        (self.trail_rect.x-(i+1)*self.scale,
                         self.trail_rect.y, self.scale, self.scale)
                    )
        elif self.dir == "l" and self.trail_rect.w >= 10 * self.scale:
            for i in range(25):
                if random.randint(0, i) < 5:
                    pygame.draw.rect(self.screen, self.trail,
                        (self.trail_rect.x+self.trail_rect.w+(i+1)*self.scale,
                         self.trail_rect.y, self.scale, self.scale)
                    )