from src.entities.player import Player
from src.entities.position import Position
from src.types.tyleTypes import TyleTypes


class Board:

    def __init__(self, width, height, walls=[], crates=[], players=[], bonuses=[], fires=[], bombs=[]):
        self.board = [[TyleTypes.NORMAL for i in range(width)] for j in range(height)]
        for wall in walls:
            self.board[wall.position.x][wall.position.y] = TyleTypes.WALL
        for crate in crates:
            self.board[crate.position.x][crate.position.y] = TyleTypes.CRATE
        for player in players:
            self.board[player.position.x][player.position.y] = player.username
        for bonus in bonuses:
            self.board[bonus.position.x][bonus.position.y] = TyleTypes.BONUS
        for fire in fires:
            self.board[fire.position.x][fire.position.y] = TyleTypes.FIRE
        for bomb in bombs:
            self.board[bomb.position.x][bomb.position.y] = TyleTypes.BOMB

    def visualize(self):
        for row in self.board:
            for col in row:
                if (type(col) == str):
                    print(col, end=" ")
                else:
                    print(col.name, end=" ")
            print()


b = Board(11, 15, players=[Player("bob", Position(1, 3))])
b.visualize()
