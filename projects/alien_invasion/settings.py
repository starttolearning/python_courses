class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self) -> None:
        """Initialize the game's settings"""
        self.caption = "Alien Invasion - Lesson 2"
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230, 230, 230)

        # Ship settings
        # self.ship_speed = 1.5
        self.ship_limit = 3

        # Bullet settings 子弹相关的设定
        # self.bullet_speed = 2.0 # 子弹的速度
        self.bullet_width = 3 # 子弹的宽度
        self.bullet_height = 15 # 子弹的高度
        self.bullet_color = (60, 60, 60) # 子弹的颜色
        self.bullets_allowed = 3

        # Alien settings
        # self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # 舰队运动方向，1代表向右，-1代表向左
        # self.fleet_direction = 1

        self.alien_points = 50
        self.score_scale = 1.5

        self.speedup_scale = 1.1


    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # 舰队运动方向，1代表向右，-1代表向左
        self.fleet_direction = 1
    
    def increase_speed(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)