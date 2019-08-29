from src.models.DQN import QNetwork
import gym


def test_QNetwork():
    parameters = {"loss_metric": "mse",
                  "learning_rate": 0.01,
                  "learning_rate_decay": 0.01,
                  "layers": [24, 24]}

    env = gym.make("CartPole-v0")
    q_network = QNetwork(env, parameters)
    model = q_network.build_q_dense_network()
    config_network = model.get_config()
    assert (config_network.get("name")[0:10] == "sequential")

    # Layers
    config_layers = config_network.get("layers")
    assert (len(
        config_layers) == 3), "You should only have 2 dense layers"

    # First layer
    assert (config_layers[0].get(
        "class_name") == "Dense"), "Incorrect layertype in first layer"
    assert (config_layers[0].get("config").get("batch_input_shape") == (
    None, q_network.observations_size))
    assert (config_layers[0].get("config").get(
        "units") == 24), "Incorrect number of neurons in first layer"
    assert (config_layers[0].get("config").get("activation") == "relu"), \
        "Activation function for first layer should be relu"

    # Second layer
    assert (config_layers[1].get(
        "class_name") == "Dense"), "Incorrect layertype in first layer"
    assert (config_layers[1].get("config").get(
        "units") == 24), "Incorrect number of neurons in first layer"
    assert (config_layers[1].get("config").get("activation") == "relu"), \
        "Activation function for second layer should be relu"

    # Thrid layer
    assert (config_layers[2].get(
        "class_name") == "Dense"), "Incorrect layertype in first layer"
    assert (config_layers[2].get("config").get(
        "units") == q_network.action_size), "Incorrect number of neurons in first layer"
    assert (config_layers[2].get("config").get(
        "activation") == "linear"), \
        "Activation function for third layer should be linear"

    config_optimizer = model.optimizer.get_config()
    assert (0.0099 < config_optimizer.get(
        "lr") <= 0.01), "Learning rate should be 0.01"
    assert (0.0099 < config_optimizer.get(
        "decay") <= 0.01), "Learning rate decay should be 0.01"
    assert (model.loss == "mse"), "Loss metric should me mse"

