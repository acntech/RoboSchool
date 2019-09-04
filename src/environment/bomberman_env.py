from src.socket.socket_client import SocketClient
import gym
from typing import Dict, Any

class BombermanEnv(gym.Env):
    def __init__(self,
                 mode: str = "TRAIN",
                 config: Dict,
                 username: str = "AIUser",
                 n_skip_frames: int = 1,
                 position: str="lower_left",):
        """
        Create a Bomberman environment.

        Arguments:
        ----------
        mode (str): Currently only "TRAIN" supported.
        config (Dict): Config parameters for the connection. Should contain the following fields:
            ip: ip-address for the connection
            port: port for the connection
            rewards: (Optional) A dict of the rewards for the outcomes.
        position (str): One of "lower_left", "lower_right", "upper_left" and "upper_right".
        """
        self.mode = mode
        self.n_skip_frames = n_skip_frames
        ip, port = config.get("ip"), config.get("port")
        self._rewards = config.get("rewards",
                             dict(
                                 action=-1,
                                 kill=100,
                                 die=-300,
                                 win=400
                             ))
        self.username = username
        self.client = SocketClient(self.username, ip, port, mode) # TODO
        # TODO: Check if a waiting period is needed here
        # Configure the rewards the game engine calculates.
        self.client.set_rewards(self._rewards)
        self.client.set_n_skip_frames(self.n_skip_frames)
        self.client.set_position(position)

    def reset(self) -> Dict[str, Any]:
        """
        Reset game and return the initial state.
        :return:
        """
        return self.client.reset()
