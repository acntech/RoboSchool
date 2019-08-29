import gym


def cartpole():
    env = gym.make("CartPole-v0")
    env.reset()
    _, _, _, _ = env.step(env.action_space.sample())
    env.close()
    return True


def pong():
    env = gym.make("PongNoFrameskip-v4")
    env.reset()
    _, _, _, _ = env.step(env.action_space.sample())
    env.close()
    return True