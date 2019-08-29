from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.optimizers import Adam


class QNetwork:

    def __init__(self, env, parameters):
        self.observations_size = env.observation_space.shape[0]
        self.action_size = env.action_space.n
        self.learning_rate = parameters["learning_rate"]
        self.learning_rate_decay = parameters["learning_rate_decay"]
        self.loss_metric = parameters["loss_metric"]
        self.hidden_layer_1 = parameters["hidden_layer_1"]
        self.hidden_layer_2 = parameters["hidden_layer_2"]

    def build_q_network(self):
        model = Sequential()
        model.add(
            Dense(self.hidden_layer_1, input_dim=self.observations_size,
                  activation='relu'))

        "Input code below"
        model.add(Dense(self.hidden_layer_2, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))

        "Input code above"

        model.compile(loss=self.loss_metric,
                      optimizer=Adam(lr=self.learning_rate,
                                     decay=self.learning_rate_decay))

        return model

'''
from keras.layers import Dense
from keras.layers import Conv2D
from keras.layers import Flatten
from keras import models
from keras import optimizers


class DQN():
    def __init__(self, input_shape, n_actions):
        self.model = models.Sequential()
        self.model.add(Conv2D(32,
                              kernel_size=8,
                              activation='relu',
                              strides=4,
                              input_shape=input_shape))

        self.model.add(Conv2D(64,
                              kernel_size=4,
                              activation='relu',
                              strides=2,
                              input_shape=input_shape))

        self.model.add(Conv2D(64,
                              kernel_size=3,
                              activation='relu',
                              strides=1,
                              input_shape=input_shape))

        self.model.add(Flatten())

        self.model.add(Dense(512, activation='relu'))

        self.model.add(Dense(n_actions, activation='linear'))

    def print_model(self):
        self.model.summary()
        '''