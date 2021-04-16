class Settings:
    """储存游戏设置"""

    def __init__(self):
        """初始化游戏的设置"""

        # 基础配置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # 飞船配置
        self.ship_speed = 5
        # 子弹配置
        self.bullet_speed = 4
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10
        # 外星人设置
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction 为 1 表示向右，为-1 表示向左
        self.fleet_direction = 1
