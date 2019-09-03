# Taken from Bomberman frontend

import socketio
import sys, time
import random
from typing import Dict, Any,  Callable # Static typing

class SocketClient:
	NAVIGATE = "NAVIGATE"
	DROP_BOMB = "DROP_BOMB"
        DO_NOTHING = "DO_NOTHING"
	GET_STATE = "AI_GET_STATE"
	TRAIN = "AI_TRAIN"
        ACTIONS = {
                "UP": 0,
                "RIGHT": 1,
                "DOWN": 2,
                "LEFT": 3,
                "DROP_BOMB": 4,
                "DO_NOTHING": 5,
                }

	def __init__(self, 
                username: str, 
                ip: str, 
                port: int, 
                mode: str = "TRAIN",
                callback: Callable = function { pass }):
            """
            Create a socket client which can either play game or collect training data.

            Arguments:
            ----------
            username (str): Unique string identifying the player.
            ip (str): The ip of the socket.io server to connect to.
            port (int): The port to connect to on the server.
            callback (Callable): Any callback
            """
            self.ip = ip
            self.port = port
            self.alive = True
            self.gameStarted = False
            self.connected = False
            self.username = username
            self.callback = callback
            self.mode = mode

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
                    if (data["username"] == self.username):
                            print("Oh no {} died!".format(data["username"]))
                            self.alive = False

	def connect(self):
		self.sio.connect("http://" + self.ip + ":" + self.port)
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
                * 0: Up
                * 1: Right
                * 2: Down
                * 3: Left
                * 4: Drop bomb
                * 5: Do nothing

            Returns:
            --------
            Tuple[Dict[str, Any], float, bool, Dict[str, Any]]: Returns a tuple of (next_state, reward, done, info).

            Raises:
            -------
            ArgumentError: If the action is not valid.
            """
            action_int = self.ACTIONS[action]
            event_type, data = None, None
            if action_int == 0: # Go up
                event_type = self.NAVIGATE
                data = {'direction': 'up', 'username': self.username }
            elif action_int == 1: # Go right
                event_type = self.NAVIGATE
                data = {'direction': 'right', 'username': self.username }
            elif action_int == 2: # Go down
                event_type = self.NAVIGATE
                data = {'direction': 'down', 'username': self.username }
            elif action_int == 3: # Go left
                event_type = self.NAVIGATE
                data = {'direction': 'left', 'username': self.username }
            elif action_int == 4: # Drop bomb
                event_type = self.DROP_BOMB
                data = {'username': self.username }
            elif action_int == 5: # Do nothing
                event_type = self.DO_NOTHING
                data = {'left', 'username': self.username }
            else: # Agument error, not in range
                raise ArgumentError(r'action must be one of ["UP", "RIGHT", "LEFT", "LEFT", "DROP_BOMB", "DO_NOTHING"]. Got {}'.format(action))
            # Send action and wait for updated state
            response =  self.sio.call(event_type, data)
            # TODO: Make API like commented line two lines below
            # 'step' means that the call requires a response
            # response = self.sio.call(event='step', data=dict(action = action.to_lower(), username = self.username))
            return process_step_result(response)

        def process_step_result(self, response: Dict[str, Any]) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
            """
            Takes the response from the frontend and decodes it into Tuple[Dict[str, Any], float, bool, Dict[str, Any]].
            """
            # TODO: Check the return with frontend and write this function
            return response['new_state'], response['reward'], response['done'], response['info']

        def reset(self):
            self.sio.emit(self.RESET)

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
