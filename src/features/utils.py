import json
from pathlib import Path

# This path will point to this file no matter where it is called from
current_file_path = Path(__file__).resolve().parent.parent

def load_param_json(env_name):
    """
    Loads hyperparameters saved as json file
    :param env_name:
    :return: hyperparameters in dict
    """

    param_path = current_file_path.joinpath('hyperparameters',
                                            env_name + '.json')
    parameters = {}
    with open(str(param_path), 'r') as f:
        parameters = json.load(f)
    return parameters


if __name__ == '__main__':
    print(load_param_json('CartPole-v1'))