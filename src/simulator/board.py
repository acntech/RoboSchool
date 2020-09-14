import numpy as np
from player import Player
from position import Position
from numba import njit


class Board:

    self.directions = [
        Position(0, 1),
        Position(0, -1),
        Position(-1, 0),
        Position(1, 0)
    ]

    def __init__(self, size):
        self.board = np.zeros((size, size))

    def get_board(self):
        return self.board

    @njit
    def get_legal_moves(self, player: Player):
        for x, y in self.directions:
            

    