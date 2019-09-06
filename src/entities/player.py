from src.types.bonusTypes import BonusTypes


class Player:

    def __init__(self, username, position, ego=False):
        self.username = username
        self.position = position
        self.stats = {BonusTypes.EXTRA_BOMB: 0, BonusTypes.SPEED: 1, BonusTypes.BOMB_POWER: 2}
        self.ego = ego

    def set_stat(self, stat, value):
        self.stats[stat] = value

    def move(self, x, y):
        self.position.x += x
        self.position.y += y

    def get_username(self):
        return self.username

