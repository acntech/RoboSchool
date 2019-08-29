import warnings
from statistics import mean
import json
from pathlib import Path
from src.features.utils import load_param_json

warnings.filterwarnings("ignore")

ENV_NAME = 'CartPole-v1'

def main():
    """
    Run print function from package
    """

    parameters = load_param_json('standard')
    print(parameters)

    print('main')


if __name__ == '__main__':
    main()
