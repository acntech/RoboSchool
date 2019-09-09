import warnings
from src.features.train_DQN import train
from src.agents.DQN_agent import DQNAgent
from src.features.utils import check_param_existence
import argparse

warnings.filterwarnings('ignore')

ENV_NAME = 'CartPole-v0'


def main(param_file):
    """
    Run print function from package
    """

    # Training settings

    episodes = 500

    iterations = 500

    dqn_agent = DQNAgent(ENV_NAME, param_file)

    train(dqn_agent, iterations, episodes)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= 'Select parameter file')
    parser.add_argument('-p', '--param', type=str,
                        default='CartPole-v0')
    args = vars(parser.parse_args())

    assert check_param_existence(args.get('param')), 'Param file does not exist'

    main(args.get('param'))
