import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from game_info import GameInfo
from scoreboard import Scoreboard


class AlienInvasion:
    def __init__(self) -> None:
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.caption)

        self.game_info = GameInfo(self, "START")

        # Create an instance to store game statistics. 
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        
        # Full screen mode
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        self.ship = Ship(self)

        # Bullets group
        self.bullets = pygame.sprite.Group()

        # Aliens group
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
    
    def _create_fleet(self):
        # 创建一个外星人并将这个外星人加入到aliens组里面去
        alien = Alien(self)
        self.aliens.add(alien)
        
        # 计算横向可以容纳多少个外星人 
        # alien_width = alien.rect.width
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # 计算纵向能容纳的外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -(3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)


        # 创建一排外星人
        # for alien_number in range(number_aliens_x):
        #     alien = Alien(self)
        #     alien.x = alien_width + 2 * alien_width * alien_number
        #     alien.rect.x = alien.x
        #     self.aliens.add(alien)
        # 创建整个舰队
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_aliens(alien_number, row_number)
                

    def _create_aliens(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def run_game(self):
        while True:
            self._check_event()

            # 当game_active为True的时候才更新游戏里面的对象
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _update_aliens(self):
        """更新所有alien的位置信息"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检测飞船和外星人的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # 检测外星人是否超出屏幕底部
        self._check_aliens_bottom()
    
    def _check_fleet_edges(self):
        """检测是否碰触边缘并且向下坠落"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """让舰队向下坠落，改变它的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        
        self.settings.fleet_direction *= -1

    def _check_event(self):
        """Respond to keypress and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.game_info.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重置
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            # 隐藏鼠标
            pygame.mouse.set_visible(False)
    

    def _check_keydown_event(self, event):
        """Events handler for keydown"""
        if event.key == pygame.K_q:
            sys.exit()
        if event.key == pygame.K_RIGHT:
            # 让飞船往右边移动
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_event(self, event):
        """Events handler for keyup"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        self.bullets.update()
        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
    

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        # Limiting the number of bullets
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        if not self.stats.game_active:
            self.game_info.blitme()

        else:
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            # 将aliens显示在屏幕上
            self.aliens.draw(self.screen)
            self.sb.show_score()
        
        # Must be the final to update the screen
        pygame.display.flip()
    
    def _ship_hit(self):
        if self.stats.ships_left > 0:
            # 生命值减少1
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            
            # 清空aliens和bullets
            self.aliens.empty()
            self.bullets.empty()

            # 创建新的fleet
            self._create_fleet()

            # 让飞船居中
            self.ship.center_ship()

            # 停一会儿重新开始
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    
    def _check_aliens_bottom(self):
        """检查外星人是否到达屏幕的最底部"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
