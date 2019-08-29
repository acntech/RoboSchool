from src.features.utils import load_param_json


def test_load_param_json():
    env_name = 'CartPole-v1'
    parameters = load_param_json(env_name)
    assert type(parameters) is dict
