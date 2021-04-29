import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        # 初始化
        pygame.init()
        # 获取参数设置
        self.settings = Settings()
        # 设置屏幕大小
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        # 设置标题
        pygame.display.set_caption("Alien Invasion")
        # 创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)
        # 获取飞船对象
        self.ship = Ship(self)
        # 创建子弹编组
        self.bullets = pygame.sprite.Group()
        # 创建外星人编组
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # 创建 Play 按钮
        self.play_button = Button(self, 'Play')

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 监视键盘和鼠标事件
            self._check_events()
            if self.stats.game_active:
                # 更新飞船位置信息
                self.ship.update()
                # 更新子弹的位置并删除消失的子弹
                self._update_bullets()
                # 更新外星人的位置
                self._update_aliens()
            # 绘制屏幕
            self._update_screen()

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.stats.ships_left > 0:
            # 将 ship_left 减1
            self.stats.ships_left -= 1
            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            # 创建一群新的外星人，并将飞船放到屏幕底端的中央
            self._create_fleet()
            self.ship.center_ship()
            # 暂停
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """监查是否有外星人到达了屏幕底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞一样处理
                self._ship_hit()
                break

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """在玩家单击 Play 按钮时开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)
            # 重置游戏统计信息
            self.stats.reset_stats()
            self.stats.game_active = True
            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            # 创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()

    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """响应松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        # 更新编组的子弹位置信息
        self.bullets.update()
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # 响应子弹和外星人碰撞
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人碰撞"""
        # 检查是否有子弹击中了外星人，如果是，就删除相应的子弹和外星人
        pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # 删除现有的子弹并新建一群外星人
            self.bullets.empty()
            self._create_fleet()

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组 bullets 中"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """创建外星人群"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # 计算一行可以容纳多少个外星人(外星人的间距为外星人宽度)
        available_space_x = self.settings.screen_width - (2 * alien_width)
        numbers_aliens_x = available_space_x // (2 * alien_width)

        # 计算屏幕可容纳多少行外星人。
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # 创建第一行外星人
        for row_number in range(number_rows):
            for alien_number in range(numbers_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人并将其放在当前行"""
        alien = Alien(self)
        alien.check_edges()
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """更新外星人群中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()
        # 外星人和飞船相撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # 检查是否有外星人到达了屏幕底端。
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """每次循环都会重绘屏幕"""
        # 绘制屏幕
        self.screen.fill(self.settings.bg_color)
        # 绘制飞船
        self.ship.blitme()
        # 绘制子弹组
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # 绘制外星人
        self.aliens.draw(self.screen)
        # 如果游戏处于非活动状态，就绘制 Play 按钮
        if not self.stats.game_active:
            self.play_button.draw_button()
        # 让最近绘制的屏幕可见。
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏。
    ai = AlienInvasion()
    ai.run_game()
