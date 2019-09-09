from enum import Enum


class ActionTypes(Enum):
    GO_UP = 1
    GO_DOWN = 2
    GO_LEFT = 3
    GO_RIGHT = 4
    PLACE_BOMB = 5
    DO_NOTHING = 0