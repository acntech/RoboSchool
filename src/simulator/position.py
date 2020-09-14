import numpy as np
from numba import njit

class Position:

    def __init__(self, x, y):
        self.position = np.array([x, y])

    @njit
    def __add__(self, o):
        return np.add(self.position, o.position)