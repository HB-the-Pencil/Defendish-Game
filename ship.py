import pygame
from settings import Settings

class Ship:
    """A class to manage the player ship."""

    def __init__(self, d_game):
        """
        Initialize the ship and its starting position.
        """
        self.settings = Settings()

        self.screen = d_game.screen
        self.screen_rect = d_game.screen.get_rect()

        # Import the ship images.
        self.images = {
            "ship_l": pygame.image.load("images/ship_l_1.png"),
            "ship_r": pygame.image.load("images/ship_r_1.png"),
        }

        # Define a direction and frame to draw different ship images.
        self.dir = "r"
        self.frame = "1"

        self.image = self.images[f"ship_{self.dir}"]
        self.image = pygame.transform.scale(self.image,
            (self.settings.player_w, self.settings.player_h)
        )
        self.rect = self.image.get_rect()

        # Move the ship to the center of the screen.
        self.rect.center = self.screen_rect.center

        # Movement flags and velocity variables.
        self.moving_r = False
        self.moving_l = False
        self.moving_u = False
        self.moving_d = False
        self.veloc_x = 0
        self.veloc_y = 0

    def draw(self):
        """
        Draw the ship to the screen.

        :return: Draws the ship image to the screen.
        """
        self.screen.blit(self.image, self.rect)

    def update(self):
        """
        Move the ship with velocity.

        :return: Updates the ship's x and y positions.
        """
        self.image = self.images[f"ship_{self.dir}"]
        self.image = pygame.transform.scale(self.image,
            (self.settings.player_w, self.settings.player_h)
        )

        # X movement.
        if self.moving_r:
            if self.veloc_x < self.settings.player_max_speed:
                self.veloc_x += self.settings.player_accel

        elif self.moving_l:
            if self.veloc_x > -self.settings.player_max_speed:
                self.veloc_x -= self.settings.player_accel

        else:
            self.veloc_x *= self.settings.player_decel
            if abs(self.veloc_x) < 0.2:
                self.veloc_x = 0

        self.rect.x += self.veloc_x

        # Y movement.
        if self.moving_u:
            if self.veloc_y > -self.settings.player_max_speed/2:
                self.veloc_y -= self.settings.player_accel * 5

        elif self.moving_d:
            if self.veloc_y < self.settings.player_max_speed/2:
                self.veloc_y += self.settings.player_accel * 5

        else:
            self.veloc_y = 0

        self.rect.y += round(self.veloc_y)

        if self.rect.y < 34 * self.settings.scale:
            self.rect.y = 34 * self.settings.scale
        elif (self.rect.y + self.rect.h) > 240 * self.settings.scale:
            self.rect.y = 240 * self.settings.scale - self.rect.h