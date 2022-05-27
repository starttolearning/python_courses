import pygame
#0 导入Sprite模块，让Alien来继承
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to manage the alien"""

    def __init__(self, ai_game) -> None:
        """Initialize the ship and set its starting postion"""
        #1 初始化被继承的Sprite
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #2 加载alien图片，获取它的矩形框
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()

        #3 重新定义alien的(x,y)坐标，将alien定位到屏幕的左上角，这样可以左右两边添加一定的空间
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #4 存储alien的横坐标
        self.x = float(self.rect.x)

    def check_edges(self):
        """碰触边缘检测，当外星人的右边大于屏幕最右边或者小于最左边时候返回真"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    
    def update(self) -> None:
        """把舰队向右边移动"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
