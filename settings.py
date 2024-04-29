class Settings:
    """A class to store all settins for Alien Invasion"""

    def __init__(self):
        """Initiatlize the game's static settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Frame rate settings
        self.frame_rate = 60

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 7.5
        self.bullet_height = 25
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 5

        # Alien settings
        self.fleet_drop_speed = 25

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        #How quickly the alien point value increase
        self.score_scale = 1.5

        self.intialize_dynamic_settings()

    def intialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed = 4.0
        self.bullet_speed = 5.0
        self.alien_speed = 2.0
        # Fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Scoring settings
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
