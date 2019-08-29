import warnings
from src.features.utils import load_param_json
import gym
from src.features.train_DQN import train
from src.features.play_DQN import play
from src.agents.DQN_agent import Agent

warnings.filterwarnings('ignore')

ENV_NAME = 'CartPole-v0'


def main():
    """
    Run print function from package
    """

    # Training settings
    episodes = 100
    iterations = 10

    # Agent and env initialization
    parameters = load_param_json(ENV_NAME)
    env = gym.make(ENV_NAME)

    dqn_agent = Agent(env, parameters)

    train(dqn_agent, env, iterations, episodes)


if __name__ == '__main__':
    main()
