class Settings:
    """储存游戏设置"""

    def __init__(self):
        """初始化游戏的设置"""
        # 基础配置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # 飞船配置
        self.ship_limit = 3
        # 子弹配置
        self.bullet_width = 50  # 子弹宽度
        self.bullet_height = 5  # 子弹高度
        self.bullet_color = (60, 60, 60)  # 子弹颜色
        self.bullets_allowed = 15  # 子弹数量
        # 外星人设置
        self.fleet_drop_speed = 10
        # 加快游戏节奏的速度
        self.speedup_scale = 1.2
        # 初始化随游戏进行而变化的设置
        self.initialize_dynamic_setting()

    def initialize_dynamic_setting(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 3.0  # 飞船移动速度
        self.bullet_speed = 3.0  # 子弹移动速度
        self.alien_speed = 2.0  # 外星人移动速度
        self.fleet_direction = 1  # 外星人移动方向。 为 1 表示向右，为-1 表示向左
        self.alien_points = 50  # 外星人的分数

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
