from src.features import bomberman_state_encoding
from src.entities.bomb import Bomb
from src.entities.crate import Crate
from src.entities.position import Position
from src.entities.fire import Fire
from src.entities.player import Player
from src.entities.wall import Wall
from src.entities.bonus import Bonus
import numpy as np

board_height = bomberman_state_encoding.BOARD_HEIGHT
board_width = bomberman_state_encoding.BOARD_WIDTH
num_images = bomberman_state_encoding.NUM_IMAGES

danger_image_solution = np.array([
    [0, 0, 0, 0, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1],
    [1, 1, 2/5-1, 1, 1, 1, 0.1/5-1],
    [2/5-1, 2/5-1, 2/5-1, 2/5-1, 1, 0.1/5-1, 0.1/5-1],
    [1, -1, 1, 1, 1, 0.2/5-1, 0.1/5-1],
    [1, -1, -1, 1, 1, 1, 0.2/5-1],
    [1, -1, 1, 1, 1, 1, 1]
])

env_image_solution = np.array([
    [1, 0, 0, 0, 0, 0, -1],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, -1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0]
])

adversary_image_solution = np.array([
    [0, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1]
])

agent_image_solution = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
])

solids_image_solution = np.array([
    [-1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, -1, 1, 0, 0],
    [0, 0, -1, -1, -1, -1, -1],
    [0, 0, 0, -1, 0, -1, 0],
    [0, 0, 1, -1, 1, 0, 0],
    [0, 0, 0, -1, 0, 0, 0],
    [0, 0, 0, -1, 0, 0, 0]
])

# Objects
bombs = []
bombs.append(Bomb(position = Position(x=2, y=4), strength = 3, timer = 2))
bombs.append(Bomb(position = Position(x=1,y=0), strength = 2, timer = 5))
bombs.append(Bomb(position = Position(x=6,y=4), strength = 1, timer = 0.1))
bombs.append(Bomb(position = Position(x=6,y=5), strength = 1, timer = 0.2))
fires = []
fires.append(Fire(position = Position(x=1,y=5)))
fires.append(Fire(position = Position(x=1,y=6)))
fires.append(Fire(position = Position(x=1,y=7)))
fires.append(Fire(position = Position(x=2,y=6)))
crates = []
crates.append(Crate(position = Position(x=0,y=0)))
crates.append(Crate(position = Position(x=3,y=2)))
crates.append(Crate(position = Position(x=3,y=3)))
crates.append(Crate(position = Position(x=3,y=4)))
crates.append(Crate(position = Position(x=3,y=5)))
crates.append(Crate(position = Position(x=3,y=6)))
crates.append(Crate(position = Position(x=3,y=7)))
crates.append(Crate(position = Position(x=2,y=3)))
crates.append(Crate(position = Position(x=3,y=3)))
crates.append(Crate(position = Position(x=4,y=3)))
crates.append(Crate(position = Position(x=5,y=3)))
crates.append(Crate(position = Position(x=6,y=3)))
crates.append(Crate(position = Position(x=5,y=4)))
walls = []
walls.append(Wall(position = Position(x=2, y=2)))
walls.append(Wall(position = Position(x=2, y=5)))
walls.append(Wall(position = Position(x=4, y=2)))
walls.append(Wall(position = Position(x=4, y=5)))
agent = Player(position = Position(1, 1), username = 'agent')
enemies = []
enemies.append(Player(position = Position(1,1), username = 'enemy_1'))
enemies.append(Player(position = Position(4,0), username = 'enemy_2'))
enemies.append(Player(position = Position(0,6), username = 'enemy_3'))
enemies.append(Player(position = Position(6,7), username = 'enemy_4'))
bonuses = []
bonuses.append(Bonus(position = Position(6, 0), type = 'BLAST_RADIUS'))
bonuses.append(Bonus(position = Position(4, 4), type = 'BLAST_RADIUS'))

def test_construct_full_state():
    state_vector = bomberman_state_encoding.construct_full_state(
        bombs = bombs,
        fires = fires,
        walls = walls,
        agent = agent,
        enemies = enemies,
        crates = crates,
        bonuses = bonuses,
        flatten = True
    )
    assert len(state_vector) == (num_images*board_width*board_height - num_images*len(walls)),\
        "Length of the flattened-full state vector is incorrect!"

def test_construct_danger_image():
    solids_image = bomberman_state_encoding.construct_solids_image(walls=walls, crates=crates)
    danger_image = bomberman_state_encoding.construct_danger_image(bombs=bombs, fires=fires, wall_image=solids_image)
    assert np.array_equal(danger_image, danger_image_solution) == True, "Danger image is incorrect!"

def test_construct_env_image():
    env_image = bomberman_state_encoding.construct_env_image(crates=crates, bonuses=bonuses)
    assert np.array_equal(env_image, env_image_solution) == True, "Environment image is incorrect!"

def test_construct_adversary_image():
    adversary_image = bomberman_state_encoding.construct_adversary_image(enemies=enemies)
    assert np.array_equal(adversary_image, adversary_image_solution) == True, "Adversary image is incorrect!"

def test_construct_agent_image():
    agent_image = bomberman_state_encoding.construct_agent_image(agent=agent)
    assert np.array_equal(agent_image, agent_image_solution) == True, "Adversary image is incorrect!"

def test_construct_solids_image():
    solids_image = bomberman_state_encoding.construct_solids_image(walls=walls, crates=crates)
    assert np.array_equal(solids_image, solids_image_solution) == True, "Adversary image is incorrect!"

# test_construct_full_state()
# test_construct_danger_image()
# test_construct_env_image()
# test_construct_adversary_image()
# test_construct_agent_image()
# test_construct_solids_image()
