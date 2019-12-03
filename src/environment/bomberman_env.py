from src.socket.socket_client import SocketClient
import re
import gym
from typing import Dict, Any, Tuple


class BombermanEnv(gym.Env):
    def __init__(self,
                 mode: str = "TRAIN",
                 config: Dict,
                 username: str = "AIUser",
                 n_skip_frames: int = 1,
                 position: str = "lower_left",):
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
        self.client = SocketClient(self.username, ip, port, mode)
        # TODO: Check if a waiting period is needed here
        # Configure the rewards the game engine calculates.
        self.client.set_position(position)
        self.alive = True

    def reset(self) -> Dict[str, Any]:
        """
        Reset game and return the initial state.
        :return:
        """
        self.alive = True
        return self.client.reset()

    def step(self, action: str) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
        """
        Do step and get next state, reward, done, and info object.
        :param action: Action to be done.
        :return: Tuple of (new_state, reward, done, info) where
            new_state: Dict[str, Any],
            reward: float,
            done: bool,
            info: Dict[str, Any]
        """
        # TODO: Check if the player died
        new_state, event_list, done, info = self.client.step(action)
        reward = self.compute_reward(event_list)
        # Check if the player died
        if self.alive == False:
            done = True
        return new_state, reward, done, info

    def compute_reward(event_list: List[str]) -> float:
        """
        Current events:
            Crate destroyed by playerX
            playerX killed by playerY
            Invalid step towards wall tried by playerX
            Invalid step towards bomb tried by playerX
            The game is won by playerX
            Bonus 'fire|speed|bomb' aquired by playerX
        """
        reward = 0.0
        regexes = dict(crate_destroyed=re.compile(r"Crate destroyed by player([^\s])"),
                       kill=re.compile(r"([^\s]) killed by ([^\s])"),
                       invalid_wall=re.compile(
                           r"Invalid step towards wall tried by ([^\s])"),
                       invalid_bomb=re.compule(
                           r"Invalid step towards bomb tried by ([^\s])"),
                       game_won=re.compile(r"The game is won by ([^\s])"),
                       bonus=re.compile(r"Bonus ([^\s]) aquired by ([^\s])")
                       )
        n_regexes = len(regexes)
        # Iterate through the event list
        for event in event_list:
            # Iterate through the regexes classifying events
            for key, reg in regexes.items():
                m = reg.match(event)

                # Check for a match
                if m is not None:
                    # Go through the various types of events and compute rewards
                    if key in ["invalid_wall", "invalid_bomb", "game_won"]:
                        playerX = m.group(1)
                        # Check if it is this player who is the owner of the event
                        if playerX == this.username:
                            reward += this._event_type_reward(key)
                    elif key == "kill":
                        p1 = m.group(1)
                        p2 = m.group(2)
                        assert p1 != p2
                        # Check if it is this player who died
                        if p1 == self.username:
                            # Set status to dead
                            self.alive = False
                            reward += this._event_type_reward("die")
                        # Check if it is this player who killed
                        elif p2 == self.username:
                            reward += this._event_type_reward("kill")
                    elif key == "bonus":
                        bonus = m.group(1)
                        player = m.group(2)
                        # Check if it is this player who is the owner of the event
                        if player == self.username:
                            reward += this._event_type_reward("bonus", bonus)
                    break
                else:
                    wrong_regexes += 1
                # Check if there was no match for any of the events in the list
                if wrong_regexes == n_regexes
                    raise ValueError(
                        f"Event {event} was not in the list of known events. (No match)")
        return reward

    def _event_type_reward(key, bonus=None) -> float:
        """
        Helper function for computing rewards
        """
        if key == "invalid_wall":
            return self._rewards.get("invalid", 0.0)
        elif key == "invalid_bomb":
            return self._rewards.get("invalid", 0.0)
        elif key == "game_won":
            return self._rewards.get("win", 400.0)
        elif key == "die":
            return self._rewards.get("die", 30.0)
        elif key == "kill":
            return self._rewards.get("kill", 30.0)
        elif key == "bonus":
            if bonus == "fire":
                return self._rewards.get("bonus", dict()).get("fire", 10.0)
            elif bonus == "speed":
                return self._rewards.get("bonus", dict()).get("speed", 10.0)
            elif bonus == "bomb":
                return self._rewards.get("bonus", dict()).get("bomb", 10.0)
            else:
                raise KeyError(
                    f"Expected bonus of one of 'fire', 'speed', 'bomb'. Got {bonus}")
        else:
            raise KeyError(
                f"Expected one of invalid_wall, invalid_bomb, game_won, die, kill or bonus. Got {key}")
