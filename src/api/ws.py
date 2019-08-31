import asyncio
import websockets
import json
# Typechecking in python
from typing import Dict, Any

from src.agents.DQN_agent import DQNAgent


def decode_message(message: str) -> Dict[str, Any]:
    """
    Helper function for decoding the message into a
    python representation.
    
    Arguments:
    ----------
    message (str): The message from the client. Should represent a json object.

    Returns:
    --------
    Dict[str, Any]: JSON object of the state.
    """
    return json.loads(message)


class WSResponder:
    """
    WSResponder is a class responsible for making a websocket interface available that can be interfaced to get the next predicted action. 
    This class is statefull so that the agent neural network can be initialized for fast response.
    """
    def __init__(self,
                 agent = DQNAgent):
        """
        Create new Instance of the WSResponder from an agent.
        Arguments:
        ----------
        agent: An agent with a function 'select_action(self, state)'.
        """
        self.agent = agent

    def get_prediction(self, 
                       state: Dict[str, Any]) -> str:
        """
        Returns a string representation of a json object
        describing the next action of the AI.
        
        Arguments:
        ----------
        state (Dict[str, Any]): The game state JSON object. 

        Returns:
        --------
        str: String representation of JSON object. Has the form
        {"action": "<action_value>"}
        """
        predicted_action = self.agent.select_action(state)
        return '{{"action": "{predicted_action}"}}'.format(predicted_action=predicted_action)
        

    async def get_action(self, 
                         websocket, path):
        """
        Endpoint for websocket communication which allows for getting AI 
        prediction for next action.

        Arguments:
        ----------
        websocket: Represents a connection. 
        path: The path of the connection.
        """
        async for message in websocket:
            # Decode the message into a state useful for the QN_agent
            state = await decode_message(message)
            # Send the decoded state to the prediction endpoint
            next_action = await self.get_prediction(state)
            # Send the predicted action to the client
            await websocket.send(next_action)

def start(agent, host="127.0.0.1", port=8765):
    """
    Start a WebSocket listener.
    """
    ws_responder = WSResponder(agent)
    start_server = websockets.serve(ws_responder.get_action, host, port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

