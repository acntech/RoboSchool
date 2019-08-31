import warnings
from src.features.train_DQN import train
from src.agents.DQN_agent import DQNAgent

warnings.filterwarnings('ignore')

ENV_NAME = 'CartPole-v0'


def test_main():

    # Training settings
    episodes = 20
    iterations = 1

    dqn_agent = DQNAgent(ENV_NAME)

    train(dqn_agent, iterations, episodes, log=False)
