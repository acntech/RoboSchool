import src.entities
import numpy as np

BOMB_MAX_TIME = 3
BOARD_HEIGHT = 11
BOARD_WIDTH = 15

# TODO: Load in a config file or something instead of having hard coded constants inside
# TODO: Send inn a dummy board and check for correctness (Visualize with ascii art, board class)
# TODO: Add powerup information (number of bombs and players speeds)

# Nice to have todos:
# TODO: Figure out a way to encode movement (aka player 2 is moving west even though he is standing in position x right now)
# TODO: Make this module compatible with conv nets aswell (dont remove walls, and dont flatten)

# LAYERS:
# - Fire and danger (e.g 0 when bomb is placed -> progress to -1 as it approaches explosion, 1 for safe)
# - Agent, crates, bonus, empty tile (0 for empty, 1 for crate, 2 for bonus, 3 for player)
# - Enemy players (0 for empty tiles, 1 for enemy)
# - Powerups ...

def construct_images(bombs, fires, walls, player, enemies, crates, bonuses):
    danger_image = construct_danger_image(bombs, fires, walls)
    player_and_env_image = construct_player_and_env_image(player, bonuses, crates, walls)
    enemy_image = construct_enemy_image(enemies, walls)
    state_vector = np.concatenate((danger_image, player_and_env_image, enemy_image))
    return state_vector

def construct_danger_image(bombs, fires, walls):
    danger_image = np.ones(BOARD_HEIGHT, BOARD_WIDTH)
    for bomb in bombs:
        x, y = bomb.position.x, bomb.position.y
        timer = bomb.timer
        str = bomb.strength

        # Mark danger in horizontal direction
        danger_radius_left = max(x - str, 0)
        danger_radius_right = min(x + str, BOARD_WIDTH - 1)
        for x_disp in range(danger_radius_left, danger_radius_right):
            danger_image[x_disp, y] = timer/BOMB_MAX_TIME - 1

        # Mark danger in vertical direction
        danger_radius_up = max(y - str, 0)
        danger_radius_down = min(y + str, BOARD_HEIGHT - 1)
        for y_disp in range(danger_radius_up, danger_radius_down):
            danger_image[x, y_disp] = timer/BOMB_MAX_TIME - 1

    for fire in fires:
        x, y = fire.position.x, fire.position.y
        danger_image[x, y] = -1
        #TODO: Add representation for how long the fire will remain on the board

    # Flatten layer and remove wall tiles
    danger_image_flatten = danger_image.flatten()
    danger_image_flatten = remove_walls_from_image(walls, danger_image_flatten)

    return danger_image_flatten

def construct_player_and_env_image(player, bonuses, crates, walls):
    player_and_env_image = np.zeros(BOARD_HEIGHT, BOARD_WIDTH)
    for crate in crates:
        player_and_env_image[crate.player.position.x, crate.position.y] = 1
    for bonus in bonuses:
        player_and_env_image[bonus.player.position.x, bonus.position.y] = 2
    player_and_env_image[player.position.x, player.position.y] = 3

    # Flatten layer and remove wall tiles
    player_and_env_image_flatten = player_and_env_image.flatten()
    player_and_env_image_flatten = remove_walls_from_image(walls, player_and_env_image_flatten)

    return player_and_env_image_flatten

def construct_enemy_image(enemies, walls):
    enemy_image = np.zeros(BOARD_HEIGHT, BOARD_WIDTH)
    for enemy in enemies:
        enemy_image[enemy.position.x, enemy.position.y] = 1
    enemy_image_flatten= enemy_image.flatten()
    enemy_image_flatten = remove_walls_from_image(walls, enemy_image_flatten)

    return enemy_image_flatten

def remove_walls_from_image(walls, image_flatten):
    new_image = image_flatten
    for wall in walls:
        index = BOARD_WIDTH * wall.position.y + wall.position.x
        new_image = np.delete(image_flatten, index)

    return new_image
