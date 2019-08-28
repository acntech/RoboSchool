from src.models.environment_testruns import cartpole


def test_cartpole():
    result_ = cartpole()
    assert result_ == True
