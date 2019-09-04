import warnings
from src.features.train_DQN import train
from src.features.play_DQN import play
from src.agents.DQN_agent import DQNAgent

warnings.filterwarnings('ignore')

ENV_NAME = 'CartPole-v0'


def main():
    """
    Run print function from package
    """

    # Training settings
    episodes = 100
    iterations = 500

    dqn_agent = DQNAgent(ENV_NAME)

    train(dqn_agent, iterations, episodes)


if __name__ == '__main__':
    main()
