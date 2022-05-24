class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self) -> None:
        """Initialize the game's settings"""
        self.caption = "Alien Invasion - Lesson 2"
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 1.5

        # Bullet settings 子弹相关的设定
        self.bullet_speed = 2.0 # 子弹的速度
        self.bullet_width = 3 # 子弹的宽度
        self.bullet_height = 15 # 子弹的高度
        self.bullet_color = (60, 60, 60) # 子弹的颜色
        self.bullets_allowed = 3