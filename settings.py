class Settings:
    """A place to store the settings for the Defender ga,e."""

    def __init__(self):
        """
        Initialize the game's settings.
        """
        # Screen settings. Doing my best to preserve the original size :D
        self.scale = 3
        self.screen_w = 292 * self.scale
        self.screen_h = 240 * self.scale
        self.bg_color = (0, 0, 0)
        self.parallax = 3

        # Player settings.
        self.player_max_speed = 5 * self.scale
        self.player_accel = self.scale / 15
        self.player_decel = 0.98

        # Lazer settings.
        self.lazer_speed = 5 * self.scale
        self.lazer_width = 3 * self.scale
        self.lazer_height = self.scale
        self.fire_limit = 5
        self.reload = 1

        self.debug = False
