class Settings:
    """A place to store the settings for Alien Invasion."""

    def __init__(self):
        """
        Initialize the game's settings.
        """
        # Screen settings. Doing my best to preserve the original size :D
        self.scale = 3
        self.screen_w = 292 * self.scale
        self.screen_h = 240 * self.scale
        self.bg_color = (220, 0, 0)

        self.player_w = 17*self.scale
        self.player_h = 6*self.scale

        self.player_max_speed = 4 * self.scale
        self.player_accel = self.player_max_speed / 36
        self.player_decel = 0.98
