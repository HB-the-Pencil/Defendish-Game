import random as r
import pygame

class Star:
    """A class to draw background stars."""
    def __init__(self, x, y, d_game):
        """
        Create a star with x, y, and size values.

        :param x: X-position of the star.
        :param y: Y-position of the star.
        :param d_game: An instance of the Defendish game.
        """
        self.screen = d_game.screen
        self.cam = d_game.cam
        self.settings = d_game.settings
        self.scale = self.settings.scale
        self.bg_w = d_game.bg_w / self.settings.parallax

        self.size = self.scale
        self.x = x
        self.x_diff = x
        self.y = y

        self.twinkle = False

    def update(self):
        """
        Move the stars with parallax.

        :return: Moves the stars left and right.
        """
        self.x = self.x_diff + self.cam.x / self.settings.parallax

        # This wasn't working very well, so scrapped for now.
        # if r.random() > 0.8 and not self.twinkle:
        #     self.twinkle = True
        # if r.random() > 0.3 and self.twinkle:
        #     self.twinkle = False

    def draw(self):
        """
        Draw the stars in the background.

        :return: Draws the stars.
        """
        if self.twinkle:
            pygame.draw.rect(self.screen, (0, 0, 0),
                (self.x, self.y, self.size, self.size)
            )

            # Draw two extra stars to create an infinite screen.
            pygame.draw.rect(self.screen, (0, 0, 0),
                (self.x - self.bg_w, self.y, self.size, self.size)
            )
            pygame.draw.rect(self.screen, (0, 0, 0),
                (self.x + self.bg_w, self.y, self.size, self.size)
            )
        else:
            pygame.draw.rect(self.screen, (255, 255, 255),
                (self.x, self.y, self.size, self.size)
            )

            # Draw two extra stars to create an infinite screen.
            pygame.draw.rect(self.screen, (255, 255, 255),
                (self.x - self.bg_w, self.y, self.size, self.size)
            )
            pygame.draw.rect(self.screen, (255, 255, 255),
                (self.x + self.bg_w, self.y, self.size, self.size)
            )