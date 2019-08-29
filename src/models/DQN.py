from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import Conv2D
from tensorflow.python.keras.layers import Flatten
from tensorflow.python.keras.optimizers import Adam

import warnings
warnings.filterwarnings('ignore')


class QNetwork:

    def __init__(self, env, parameters):
        self.observations_size = env.observation_space.shape[0]
        self.action_size = env.action_space.n
        self.learning_rate = parameters["learning_rate"]
        self.learning_rate_decay = parameters["learning_rate_decay"]
        self.loss_metric = parameters["loss_metric"]
        self.layers = parameters['layers']
        self.input_shape = parameters.get('input_shape')

    def build_q_dense_network(self):
        self.model = Sequential()
        self.model.add(
            Dense(self.layers[0], input_dim=self.observations_size,
                  activation='relu'))

        self.model.add(Dense(self.layers[1], activation='relu'))
        self.model.add(Dense(self.action_size, activation='linear'))
        self.model.compile(loss=self.loss_metric,
                      optimizer=Adam(lr=self.learning_rate,
                                     decay=self.learning_rate_decay))

        return self.model

    def build_q_dense_from_json(self):
        self.model = Sequential()

        len_layers = len(self.layers)
        assert len_layers >= 2, 'You must have a network of \
                                            at least 2 layers'

        for i, units in enumerate(self.layers):

            if i == 0:
                self.model.add(
                    Dense(units=units,
                          input_dim=self.observations_size,
                          activation='relu',
                          name='Input_state'))

            else:
                self.model.add(
                    Dense(units=units,
                          activation='relu',
                          name='Hidden_layer'))

            if i + 1 == len_layers:
                break

        self.model.add(Dense(self.action_size,
                             activation='linear',
                             name='Output_Q_action'))

        self.model.compile(loss=self.loss_metric,
                           optimizer=Adam(lr=self.learning_rate,
                           decay=self.learning_rate_decay))

        return self.model

    def build_q_CNN(self):

        self.model = Sequential()

        self.model.add(Conv2D(32,
                              kernel_size=8,
                              activation='relu',
                              strides=4,
                              input_shape=self.input_shape))

        self.model.add(Conv2D(64,
                              kernel_size=4,
                              activation='relu',
                              strides=2))

        self.model.add(Conv2D(64,
                              kernel_size=3,
                              activation='relu',
                              strides=1))

        self.model.add(Flatten())

        self.model.add(Dense(512, activation='relu'))

        self.model.add(Dense(self.action_size, activation='linear'))

        self.model.compile(loss=self.loss_metric,
                           optimizer=Adam(lr=self.learning_rate,
                           decay=self.learning_rate_decay))

        return self.model

