import src.entities
import numpy as np

BOMB_MAX_TIME = 3
BOARD_HEIGHT = 11
BOARD_WIDTH = 15

# TODO: Load in a config file or something instead of having hard coded constants inside
# TODO: Send inn a dummy board and check for correctness (Visualize with ascii art, board class)
# TODO: Add powerup information (number of bombs the agent has left and players speeds)

# Nice to have todos:
# TODO: Figure out a way to encode movement (aka player 2 is moving west even though he is standing in position x right now)
# TODO: Make this module compatible with conv nets aswell (dont remove walls, and dont flatten)

# LAYERS:
# - Fire and danger (e.g 0 when bomb is placed -> progress to -1 as it approaches explosion, 1 for safe)
# - Crates, bonus, empty tile (-1 for bonus, 0 for empty, 1 for create)
# - The agent and enemy players (-1 for enemy, 0 for empty tiles, 1 for player)
# - Powerups ... (not implemented)

def construct_flattened_images_state(bombs, fires, walls, agent, enemies, crates, bonuses):
    danger_image = construct_danger_image(bombs, fires, walls)
    env_image = construct_env_image(bonuses, crates, walls)
    agent_image = construct_agent_image(agent, walls)
    adversary_image = construct_adversary_image(enemies, walls)
    state_vector = np.concatenate((danger_image, env_image, agent_image, adversary_image))
    return state_vector

def construct_danger_image(bombs, fires, walls):
    danger_image = np.ones(BOARD_HEIGHT, BOARD_WIDTH)
    for bomb in bombs:
        # Mark danger in horizontal direction
        danger_radius_left = max(bomb.position.x - bomb.strength, 0)
        danger_radius_right = min(bomb.position.x + bomb.strength, BOARD_WIDTH - 1)
        for x_disp in range(danger_radius_left, danger_radius_right):
            danger_image[x_disp, bomb.postion.y] = bomb.timer/BOMB_MAX_TIME - 1

        # Mark danger in vertical direction
        danger_radius_up = max(bomb.position.y - bomb.strength, 0)
        danger_radius_down = min(bomb.position.y + bomb.strength, BOARD_HEIGHT - 1)
        for y_disp in range(danger_radius_up, danger_radius_down):
            danger_image[bomb.position.x, y_disp] = bomb.timer/BOMB_MAX_TIME - 1

    for fire in fires:
        danger_image[fire.position.x, fire.position.y] = -1
        #TODO: Add representation for how long the fire will remain on the board

    # Flatten layer and remove wall tiles
    danger_image_flatten = danger_image.flatten()
    danger_image_flatten = remove_walls_from_image(walls, danger_image_flatten)

    return danger_image_flatten

def construct_env_image(bonuses, crates, walls):
    env_image = np.zeros(BOARD_HEIGHT, BOARD_WIDTH)
    for crate in crates:
        env_image[crate.position.x, crate.position.y] = 1
    for bonus in bonuses:
        env_image[bonus.position.x, bonus.position.y] = -1

    # Flatten layer and remove wall tiles
    env_image_flatten = env_image.flatten()
    env_image_flatten = remove_walls_from_image(walls, env_image_flatten)

    return env_image_flatten

def construct_adversary_image(enemies, walls):
    enemy_image = np.zeros(BOARD_HEIGHT, BOARD_WIDTH)
    for enemy in enemies:
        enemy_image[enemy.position.x, enemy.position.y] = 1
    enemy_image_flatten= enemy_image.flatten()
    enemy_image_flatten = remove_walls_from_image(walls, enemy_image_flatten)

    return enemy_image_flatten

def construct_agent_image(agent, walls):
    agent_image = np.zeros(BOARD_HEIGHT, BOARD_WIDTH)
    agent_image[agent.position.x, agent.position.y] = 1
    agent_image_flatten= agent_image.flatten()
    agent_image_flatten = remove_walls_from_image(walls, agent_image_flatten)

    return agent_image_flatten

def construct_powerup_vector(agent, enemies):
    raise NotImplemented()

def remove_walls_from_image(walls, image_flatten):
    new_image = image_flatten
    for wall in walls:
        index = BOARD_WIDTH * wall.position.y + wall.position.x
        new_image = np.delete(new_image, index)
    return new_image
