
class GameStats:
    """记录所有游戏状态信息"""
    def __init__(self, ai_game): 
        """初始化""" 
        self.settings = ai_game.settings 
        self.reset_stats()

        self.game_active = False

        # 最高分
        self.high_score = 0
    
    def reset_stats(self):
        """改变初始信息.""" 
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1