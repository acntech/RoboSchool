import src.entities

def image_layers(self, board):
    # LAYERS:
    # - Fire and danger (e.g 0 when bomb is placed -> progress to -1 as it approaches explosion, 1 for safe)
    # - Agent/players (e.g discrete numbers 0-3 for players and 4 for empty squares)
    # - Walls and bonuses (-1 for wall, 1 for bonus)
    # - Powerup status for all players (Vector of size 3 (bombs, speed, fireradius), 1 for each player)

    #TODO: Create the different image layers given board
    #TODO: Send inn a dummy board and check for correctness (Visualize with ascii art)
    #TODO: Return flattended array (layers + powerup vectors) for input to NN
    pass
