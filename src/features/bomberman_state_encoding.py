import numpy as np

BOMB_MAX_TIME = 5
BOARD_HEIGHT = 8
BOARD_WIDTH = 7
NUM_IMAGES = 4

# TODO: Load in a config file or something instead of having hard coded constants for board height/width and max bomb time

# Nice to have todos:
# TODO: Figure out a way to encode movement (aka player 2 is moving west even though he is standing in position x right now)
# TODO: Add representation for how long the fire will remain on the board
# TODO: Add powerup information (number of bombs the agent has left, the agents speed, and other players bombs available)
# TODO: Implement a relative state vector that encodes information locally and relative to the agents position (reduced state vector)

# LAYERS:
# - Fire and danger (e.g 0 when bomb is placed -> progress to -1 as it approaches explosion, 1 for safe)
# - Crates, bonus, empty tile (-1 for bonus, 0 for empty, 1 for create)
# - Adversaries (1 for enemy, 0 for not)
# - Player position (1 for current position, 0 for not)

def construct_full_state(bombs, fires, walls, agent, enemies, crates, bonuses, flatten = True):
    images = []
    solids_image = construct_solids_image(walls, crates) # for help to construct danger_image only
    images.append(construct_danger_image(bombs, fires, solids_image))
    images.append(construct_env_image(bonuses, crates))
    images.append(construct_agent_image(agent))
    images.append(construct_adversary_image(enemies))
    if flatten:
        state_vector = np.concatenate([flatten_image(image, walls) for image in images])
    else:
        state_vector = np.dstack((image for image in images))
    return state_vector

def construct_relative_state():
    return NotImplemented()

def construct_danger_image(bombs, fires, wall_image):
    danger_image = np.ones((BOARD_HEIGHT, BOARD_WIDTH))
    bombs_timer_sorted = sorted(bombs, key=lambda bomb: bomb.timer, reverse=True) # sort on ascending timers
    for bomb in bombs_timer_sorted:
        # Mark danger in horizontal direction
        danger_most_left = max(bomb.position.x - bomb.strength, 0)
        danger_most_right = min(bomb.position.x + bomb.strength, BOARD_WIDTH - 1)
        for x in range(bomb.position.x, danger_most_left - 1, -1):
            if(wall_image[bomb.position.y, x] == 1):
                break
            else:
                danger_image[bomb.position.y, x] = bomb.timer/BOMB_MAX_TIME - 1
            if(wall_image[bomb.position.y, x] != 0):
                break
        for x in range(bomb.position.x, danger_most_right + 1, 1):
            if(wall_image[bomb.position.y, x] == 1):
                break
            else:
                danger_image[bomb.position.y, x] = bomb.timer / BOMB_MAX_TIME - 1
            if (wall_image[bomb.position.y, x] != 0):
                break

        # Mark danger in vertical direction
        danger_most_up = max(bomb.position.y - bomb.strength, 0)
        danger_most_down = min(bomb.position.y + bomb.strength, BOARD_HEIGHT - 1)
        for y in range(bomb.position.y, danger_most_up - 1, -1):
            if(wall_image[y, bomb.position.x] == 1):
                break
            else:
                danger_image[y, bomb.position.x] = bomb.timer/BOMB_MAX_TIME - 1
            if(wall_image[y, bomb.position.x] != 0):
                break
        for y in range(bomb.position.y, danger_most_down + 1, 1):
            if(wall_image[y, bomb.position.x] == 1):
                break
            else:
                danger_image[y, bomb.position.x] = bomb.timer/BOMB_MAX_TIME - 1
            if(wall_image[y, bomb.position.x] != 0):
                break

    for fire in fires:
        danger_image[fire.position.y, fire.position.x] = -1

    return danger_image

def construct_env_image(bonuses, crates):
    env_image = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))
    for crate in crates:
        env_image[crate.position.y, crate.position.x] = 1
    for bonus in bonuses:
        env_image[bonus.position.y, bonus.position.x] = -1
    return env_image

def construct_adversary_image(enemies):
    enemy_image = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))
    for enemy in enemies:
        enemy_image[enemy.position.y, enemy.position.x] = 1
    return enemy_image

def construct_agent_image(agent):
    agent_image = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))
    agent_image[agent.position.y, agent.position.x] = 1
    return agent_image

def construct_solids_image(walls, crates):
    solids_image = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))
    for wall in walls:
        solids_image[wall.position.y, wall.position.x] = 1
    for crate in crates:
        solids_image[crate.position.y, crate.position.x] = -1
    return solids_image

def construct_powerup_vector(agent, enemies):
    raise NotImplemented()

def remove_walls_from_image(walls, image_flatten):
    new_image = image_flatten
    for wall in walls:
        index = BOARD_WIDTH * wall.position.y + wall.position.x
        new_image = np.delete(new_image, index)
    return new_image

def flatten_image(image, walls):
    image_flatten = image.flatten()
    image_flatten_no_walls = remove_walls_from_image(walls=walls, image_flatten=image_flatten)
    return image_flatten_no_walls

def visualize_image(image):
    ydim, xdim = image.shape
    for y in range(0, ydim):
        for x in range(0, xdim):
            print(image[y, x], end = "   ")
        print()
