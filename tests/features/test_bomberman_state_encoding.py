from src.features import bomberman_state_encoding
from src.entities.bomb import Bomb
from src.entities.crate import Crate
from src.entities.position import Position
from src.entities.fire import Fire
from src.entities.player import Player
from src.entities.wall import Wall
from src.entities.bonus import Bonus
import numpy as np

danger_image_solution = np.array([
    [0, 0, 0, 0, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1],
    [1, 1, 3/5-1, 1, 1, 1, 0.1/5-1],
    [3/5-1, 3/5-1, 3/5-1, 3/5-1, 3/5-1, 0.1/5-1, 0.1/5-1],
    [1, 1, 1, 1, 1, 1, 0.1/5-1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1]
])

# Objects
bombs = []
bombs.append(Bomb(position = Position(1,0), strength = 2, timer = 5))
bombs.append(Bomb(position = Position(2,4), strength = 3, timer = 2))
bombs.append(Bomb(position = Position(6,4), strength = 1, timer = 0.1))
fires = []
fires.append(Fire(position = Position(5, 1)))
fires.append(Fire(position = Position(6, 1)))
fires.append(Fire(position = Position(7, 1)))
fires.append(Fire(position = Position(6, 2)))
crates = []
crates.append(Crate(position = Position(0,0)))
crates.append(Crate(position = Position(3,2)))
crates.append(Crate(position = Position(3,3)))
crates.append(Crate(position = Position(3,4)))
crates.append(Crate(position = Position(3,5)))
crates.append(Crate(position = Position(3,6)))
crates.append(Crate(position = Position(2,3)))
crates.append(Crate(position = Position(3,3)))
crates.append(Crate(position = Position(4,3)))
crates.append(Crate(position = Position(5,3)))
crates.append(Crate(position = Position(6,3)))
walls = []
walls.append(Wall(position = Position(2, 2)))
walls.append(Wall(position = Position(2, 4)))
walls.append(Wall(position = Position(5, 2)))
walls.append(Wall(position = Position(5, 4)))
player = Player(position = Position(1, 1), username = 'agent')
enemies = []
enemies.append(Player(position = Position(1, 1), username = 'enemy_1'))
enemies.append(Player(position = Position(0, 4), username = 'enemy_2'))
enemies.append(Player(position = Position(6, 0), username = 'enemy_3'))
enemies.append(Player(position = Position(7, 6), username = 'enemy_4'))
bonuses = []
bonuses.append(Bonus(position = Position(0, 6), type = 'BLAST_RADIUS'))
bonuses.append(Bonus(position = Position(4, 4), type = 'BLAST_RADIUS'))

state_vector = bomberman_state_encoding.construct_flattened_images_state(
    bombs = bombs,
    fires = fires,
    walls = walls,
    agent = player,
    enemies = enemies,
    crates = crates,
    bonuses = bonuses
)

print(state_vector)
print(len(state_vector))