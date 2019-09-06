class Bomb:

    def __init__(self, position, strength, timer, origin=""):
        self.position = position
        self.strength = strength
        self.timer = timer
        self.origin = origin

    def get_origin(self):
        return self.origin