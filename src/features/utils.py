import json
from pathlib import Path
import pytz
import datetime

# This path will point to this file no matter where it is called from
current_file_path = Path(__file__).resolve().parent.parent


def check_param_existence(param):
    param_path = current_file_path.joinpath('hyperparameters',
                                            param + '.json')
    return param_path.exists()


def load_param_json(env_name):
    """
    Loads hyperparameters saved as json file
    :param env_name:
    :return: hyperparameters in dict
    """

    param_path = current_file_path.joinpath('hyperparameters',
                                            env_name + '.json')

    with open(str(param_path), 'r') as f:
        parameters = json.load(f)
    return parameters


def check_available_GPU():
    from tensorflow.python.client import device_lib
    print(device_lib.list_local_devices())


def generate_timestamp():
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("Europe/Oslo"))
    return pst_now.strftime('%Y-%m-%d_%H-%M-%S')


if __name__ == '__main__':
    check_available_GPU()
