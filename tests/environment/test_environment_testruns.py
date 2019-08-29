from src.environment.environment_testruns import cartpole
from src.environment.environment_testruns import pong


def test_cartpole():
    result_ = cartpole()
    assert result_ == True


def test_pong():
    result = pong()
    assert result == True
