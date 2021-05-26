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
        # 准备包含最高得分和当前得分的图像
        self.prep_score()
        self.prep_high_score()

    def prep_score(self):
        """将得分转化成一幅渲染的图像"""
        rounded_score = round(self.stats.score, -1)  # 将分数取10的倍数
        score_str = "{:,}".format(rounded_score)  # 获取游戏分数，并转为字符串
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)  # 游戏分数转为图像
        # 在屏幕右上角显示得分
        self.score_rect = self.score_image.get_rect()  # 获取一个 Rect
        self.score_rect.right = self.screen_rect.right - 20  # 设置 Rect 的右边距
        self.score_rect.top = 20  # 设置 Rect 的上边距

    def prep_high_score(self):
        """将最高分转化为渲染的图像"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)  # 获取游戏分数，并转为字符串
        self.high_score_image = self.font.render(high_score_str, True, self.text_color,
                                                 self.settings.bg_color)  # 游戏分数转为图像
        # 在最高分放在屏幕顶部中央。
        self.high_score_rect = self.high_score_image.get_rect()  # 获取一个 Rect
        self.high_score_rect.centerx = self.screen_rect.centerx  # 设置 Rect 的中心位置的 X 轴
        self.high_score_rect.top = self.score_rect.top   # 设置 Rect 的上边距

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)  # 显示当前分数
        self.screen.blit(self.high_score_image, self.high_score_rect)  # 显示最高得分

    def check_high_score(self):
        """检查是否诞生了新的最高得分"""
        if self.stats.score > self.stats.high_score:
            # 如果当前分数比最高分数高
            self.stats.high_score = self.stats.score  # 更新最高分数
            self.prep_high_score()  # 设置最高分数的渲染参数
