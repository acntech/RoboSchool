from src.features.env_wrappers import make_env


def test_make_env():
    ENV_NAME = "PongNoFrameskip-v4"
    env = make_env(ENV_NAME)
    env.reset()
    print('Test passed')