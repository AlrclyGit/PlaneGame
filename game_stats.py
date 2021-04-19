class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        # 初始化在游戏运行期间可能变化的统计信息
        self.ships_left = self.settings.ship_limit

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""

