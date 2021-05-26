import pygame.font


class Scoreboard:
    """显示得分信息的类"""

    def __init__(self, ai_game):
        """初始化显示得分涉及的属性"""
        self.screen = ai_game.screen  # 获取游戏屏幕
        self.screen_rect = self.screen.get_rect()  # 获取游戏屏幕的居中属性
        self.settings = ai_game.settings  # 获取游戏设置
        self.stats = ai_game.stats  # 获取游戏统计类
        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # 准备初始得分图像
        self.prep_score()

    def prep_score(self):
        """将得分转化成一幅渲染的图像"""
        score_str = str(self.stats.score)  # 获取游戏分数，并转为字符串
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)  # 游戏分数转为图像
        # 在屏幕右上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
