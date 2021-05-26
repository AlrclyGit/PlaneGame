class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        # 游戏活动状态标识
        self.game_active = False
        # 初始化在游戏运行期间可能变化的统计信息
        self.reset_stats()
        # 仁和情况下都不应该重置最高得分
        self.high_score = 0

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit
        self.score = 0  # 游戏分数记录
        self.level = 1  # 当前游戏等级
