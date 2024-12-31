import pygame
from settings import Settings
from cam import Camera
import random as r

class Ship:
    """A class to manage the player ship."""

    def __init__(self, d_game):
        """
        Initialize the ship and its starting position.

        :param d_game: The game that is currently running.
        """
        self.settings = Settings()

        self.scale = self.settings.scale

        self.screen = d_game.screen
        self.screen_rect = d_game.screen.get_rect()

        self.cam = Camera(self.screen_rect.x, self.screen_rect.y, self.screen_rect.width,
            self.screen_rect.height
        )

        # Import the ship images.
        self.images = {
            "ship_l": pygame.image.load("images/ship_l.png"),
            "ship_r": pygame.image.load("images/ship_r.png"),
        }

        # Define a direction and frame to draw different ship images.
        self.dir = "r"
        self.frame = "1"

        self.image = self.images[f"ship_{self.dir}"]
        self.image = pygame.transform.scale(self.image,
            (self.scale * 17, self.scale * 6)
        )
        self.rect = self.image.get_rect()

        # Move the ship to the center of the screen.
        self.rect.x = 60 * self.scale

        self.rect.y = self.screen_rect.height//2

        # Movement flags and velocity variables.
        self.moving_r = False
        self.moving_l = False
        self.moving_u = False
        self.moving_d = False
        self.veloc_x = 0
        self.veloc_y = 0

        self.flip_x = 0

        self.x = self.rect.x
        self.y = self.rect.y

        self.w = self.rect.w
        self.h = self.rect.h

    def draw(self):
        """
        Draw the ship to the screen.

        :return: Draws the ship image to the screen.
        """
        self.screen.blit(self.image, self.rect)

        flame_colors = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0),
            (255, 0, 255),
            (0, 255, 255),
        ]

        # Draw the flames.
        if self.moving_r:
            for i in range(5):
                for j in range(10):

                    # 50% chance for a pixel to be off.
                    if r.random() < 0.5:
                        continue

                    # Shape the flame into a point.
                    if (((i == 0 or i == 4) and j > 2) or
                            ((i == 1 or i == 3) and j > 6)):
                        break

                    rectx = self.x - self.scale - j * self.scale
                    recty = self.y + i * self.scale + self.scale

                    pygame.draw.rect(self.screen, r.choice(flame_colors),
                        (rectx, recty, self.scale, self.scale)
                    )

        elif self.dir == "r":
            for i in range(5):
                for j in range(2):

                    # 50% chance for a pixel to be off.
                    if r.random() < 0.5:
                        continue

                    rectx = self.x - self.scale - j * self.scale
                    recty = self.y + i * self.scale + self.scale

                    pygame.draw.rect(self.screen, r.choice(flame_colors),
                        (rectx, recty, self.scale, self.scale)
                    )

        # Left-facing flames.
        elif self.moving_l:
            for i in range(5):
                for j in range(10):

                    # 50% chance for a pixel to be off.
                    if r.random() < 0.5:
                        continue

                    # Shape the flame into a point.
                    if (((i == 0 or i == 4) and j > 2) or
                            ((i == 1 or i == 3) and j > 6)):
                        break

                    rectx = self.x + j * self.scale + self.w
                    recty = self.y + i * self.scale + self.scale

                    pygame.draw.rect(self.screen, r.choice(flame_colors),
                        (rectx, recty, self.scale, self.scale)
                    )

        elif self.dir == "l":
            for i in range(5):
                for j in range(2):

                    # 50% chance for a pixel to be off.
                    if r.random() < 0.5:
                        continue

                    rectx = self.x + j * self.scale + self.w
                    recty = self.y + i * self.scale + self.scale

                    pygame.draw.rect(self.screen, r.choice(flame_colors),
                        (rectx, recty, self.scale, self.scale)
                    )

        if self.settings.debug:
            pygame.draw.rect(self.screen, (255, 0, 0),
                (self.x, self.y, self.w, self.h), self.scale
            )

    def update(self):
        """
        Move the ship with velocity.

        :return: Updates the ship's x and y positions.
        """
        # Update the ship based on the direction it's facing.
        self.image = self.images[f"ship_{self.dir}"]
        self.image = pygame.transform.scale(self.image,
            (self.scale * 17, self.scale * 6)
        )

        # X movement.
        if self.moving_r:
            self.dir = "r"

            if self.veloc_x < self.settings.player_max_speed:
                if self.veloc_x < 0:
                    self.veloc_x *= 0.5 # verify in arcade
                self.veloc_x += self.settings.player_accel

        elif self.moving_l:
            self.dir = "l"

            if self.veloc_x > -self.settings.player_max_speed:
                if self.veloc_x > 0:
                    self.veloc_x *= 0.5 # verify in arcade
                self.veloc_x -= self.settings.player_accel

        else:
            self.veloc_x *= self.settings.player_decel
            if abs(self.veloc_x) < 0.1:
                self.veloc_x = 0

        # Flip the player when they turn.
        if self.dir == "r":
            if self.x + self.w > 146 * self.scale:
                self.flip_x = self.settings.player_max_speed

            if self.x + self.w > 60 * self.scale:
                self.x -= self.flip_x / 1.5
                self.cam.x -= self.flip_x / 1.75
                self.flip_x *= self.settings.player_decel-0.02

        elif self.dir == "l":
            if self.x < 146 * self.scale:
                self.flip_x = -self.settings.player_max_speed

            if self.x < 232 * self.scale:
                self.x -= self.flip_x / 1.5
                self.cam.x -= self.flip_x / 1.75
                self.flip_x *= self.settings.player_decel-0.02


        # Keep the player within the left/right boundaries.
        if self.x < 60 * self.scale:
            self.x = 60 * self.scale

        if self.x > 232 * self.scale - self.w:
            self.x = 232 * self.scale - self.w

        if abs(self.flip_x) < 0.1:
            self.flip_x = 0

        # Y movement.
        if self.moving_u:
            if self.veloc_y > -self.settings.player_max_speed/2:
                self.veloc_y -= self.settings.player_accel * 5

        elif self.moving_d:
            if self.veloc_y < self.settings.player_max_speed/2:
                self.veloc_y += self.settings.player_accel * 5

        else:
            self.veloc_y *= 0.2
            if abs(self.veloc_y) < 0.1:
                self.veloc_y = 0

        self.y += self.veloc_y

        # Constrain the y.
        if self.y < 34 * self.scale:
            self.y = 34 * self.scale

        elif (self.y + self.h) > 200 * self.scale:
            self.y = 200 * self.scale - self.h

        self.rect.x = self.x
        self.rect.y = self.y

        self.cam.move(-self.veloc_x, 0)
