# Taken from Bomberman frontend

import socketio
import sys, time
import random
from typing import Dict, Any, Tuple, Callable # Static typing


def process_step_result(response: Dict[str, Any]) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
    """
    Takes the response from the frontend and decodes it into Tuple[Dict[str, Any], float, bool, Dict[str, Any]].
    """
    return response['new_state'], response['event_list'], response['done'], response['info']


class SocketClient:
    NAVIGATE = "NAVIGATE"
    DROP_BOMB = "DROP_BOMB"
    DO_NOTHING = "DO_NOTHING"
    GET_STATE = "AI_GET_STATE"
    TRAIN = "AI_TRAIN"
    ACTIONS = {
        "UP": "up",
        "RIGHT": "right",
        "DOWN": "down",
        "LEFT": "left",
        "DROP_BOMB": "bomb",
        "DO_NOTHING": "idle",
    }

    def __init__(self,
                 username: str,
                 ip: str,
                 port: int,
                 mode: str = "TRAIN",
                 callback: Callable = lambda *args: None ):
        """
        Create a socket client which can either play game or collect training data.

        Arguments:
        ----------
        username (str): Unique string identifying the player.
        ip (str): The ip of the socket.io server to connect to.
        port (int): The port to connect to on the server.
        callback (Callable): Any callback
        """
        self.username = username
        self.ip = ip
        self.port = port
        self.mode = mode

        self.alive = True
        self.gameStarted = False
        self.connected = False

        self.callback = callback
        self.state = None

        self.sio = socketio.Client()

        @self.sio.on('connect')
        def connect():
            self.connected = True
            print('connected')

        @self.sio.on('disconnect')
        def disconnect():
            self.connected = False
            print('disconnected')

        @self.sio.on('AI_STATE')
        def evaluateState(data):
            self.callback(data)

        @self.sio.on('GAME_START')
        def startGame(data):
            self.gameStarted = True

        @self.sio.on('GAME_OVER')
        def startGame(data):
            print("{} won!".format(data["winner"]))

        @self.sio.on('PLAYER_DEAD')
        def amIDead(data):
            if data["username"] == self.username:
                print("Oh no {} died!".format(data["username"]))
                self.alive = False

    def connect(self):
        self.sio.connect("http://" + self.ip + ":" + str(self.port))
        time.sleep(0.2)
        if self.mode == "TRAIN":
            self.sio.emit(self.TRAIN, {'username': self.username})

    def step(self, action: str) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
        """
        Make an action (send to server) and get the next state, reward, done, and info.

        Arguments:
        ----------
        action (str): The requested action.
        It is defined as follows:
            * "up": Up
            * "right": Right
            * "down": Down
            * "left": Left
            * "bomb": Drop bomb
            * "idle": Do nothing

        Returns:
        --------
        Tuple[Dict[str, Any], float, bool, Dict[str, Any]]: Returns a tuple of (next_state, reward, done, info).

        Raises:
        -------
        ArgumentError: If the action is not valid.
        """
        # TODO: Make API like commented line two lines below
        # 'step' means that the call requires a response
        # TODO in frontend
        response = self.sio.call(event='AI_STEP', 
                                 data=dict(action = action.to_lower(), 
                                           username = self.username, 
                                           skip_frames=self.skip_frames))
        return process_step_result(response)

    def reset(self) -> Dict[str, Any]:
        # TODO in frontend
        return self.sio.call("RESET")

    def set_position(self, position: str) -> None:
        """
        Set the position of the AI player. Can be one of "lower|upper" + _ + "left|right".
        :param str:
        :return:
        """
        # TODO in frontend
        self.sio.emit("SET_POSITION", dict(position=position))

    def request_state(self):
        """
        Send a request for the next state.
        This will later trigger the callback function.
        """
        self.sio.emit(self.GET_STATE, {'username': self.username})

    def go_left(self):
        self.sio.emit(self.NAVIGATE, {'direction': 'left', 'username': self.username})

    def go_right(self):
        self.sio.emit(self.NAVIGATE, {'direction': 'right', 'username': self.username})

    def go_up(self):
        self.sio.emit(self.NAVIGATE, {'direction': 'up', 'username': self.username})

    def go_down(self):
        self.sio.emit(self.NAVIGATE, {'direction': 'down', 'username': self.username})

    def drop_bomb(self):
        self.sio.emit(self.DROP_BOMB, {'username': self.username})

    def do_nothing(self):
        self.sio.emit(self.DO_NOTHING, {'username': self.username})

    def disconnect(self):
        self.sio.disconnect()
