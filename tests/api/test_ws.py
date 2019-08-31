from src.api.ws import WSResponder, start
import pytest
import websockets

class MockAgent():
    def __init__(self):
        return
    def select_action(self, state):
        return 1
agent = MockAgent()

def test_WSResponder_get_prediction():
    """
    Test if the WSResponder method 'get_prediction(state)' gives the correct prediction.
    """
    ws_responder = WSResponder(agent)
    state = dict()
    predicted_action = ws_responder.get_prediction(state)
    assert predicted_action == '{"action": "1"}'


# TODO: Fix this test
@pytest.mark.skip(reason="Not sure how to test the async behaviour of the server without losing control of the test flow.")
def test_WSResponder_get_action():
    """
    Test if the websocket server responds and gives a prediction when state is given.
    """
    port = 8766
    host = "127.0.0.1"
    uri = "ws://{}:{}".format(host, port)
    # Start websocket
    start(agent, port)
    # Create dummy state
    state = dict(some_state_var=123)
    state_str = json.dumps(state)

    # Connect a client websocket
    websocket = websockets.connect(uri)
    websocket.send(message)
    predicted_action = websocket.recv()
    assert predicted_action == '{"action": "1"}'
