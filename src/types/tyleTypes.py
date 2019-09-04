from enum import Enum


class TyleTypes(Enum):
    NORMAL = "o"
    BOMB = "x"
    WALL = "w"
    CRATE = "c"
    FIRE = "f"
    BONUS = "b"