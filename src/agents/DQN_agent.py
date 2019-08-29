import os
import datetime
import numpy as np

from src.models.DQN import QNetwork
from src.features.experience_buffer import ExperienceReplay


class Agent:

    def __init__(self, env, parameters):
        self.env = env
        self.local_network = QNetwork(env,
                                      parameters).build_q_dense_from_json()
        self.target_network = QNetwork(env,
                                       parameters).build_q_dense_from_json()

        self.experience_replay = ExperienceReplay(parameters)

        self.epsilon = parameters["epsilon_init"]
        self.epsilon_decay = parameters["epsilon_decay"]
        self.epsilon_minimum = parameters["epsilon_minimum"]
        self.tau = parameters["tau"]
        self.gamma = parameters["gamma"]
        self.epochs = parameters["epochs"]

    def learn(self):
        states, actions, rewards, dones, next_states = self.experience_replay.get_batch()

        # Get Q-values for the next state, Q(next_state), using the target network
        Q_target = self.target_network.predict(next_states)

        # Apply Q-learning algorithm  and Q-value for next state to calculate the actual Q-value the Q(state)
        Q_calc = rewards + (self.gamma * np.amax(Q_target,
                            axis=1).reshape(-1,1) * (1 - dones))

        # Calculate Q-value Q(state) we predicted earlier using the local network
        Q_local = self.local_network.predict(states)

        # Update Q_values with "correct" Q-values calculated using the Q-learning algorithm
        for row, col_id in enumerate(actions):
            Q_local[row, col_id.item()] = Q_calc[row]

        # Train network by minimizing the difference between Q_local and modified Q_local
        self.local_network.fit(states, Q_local, epochs=self.epochs,
                               verbose=0)

    def update_target_network(self):
        local_weights = self.local_network.get_weights()
        target_weights = self.target_network.get_weights()

        for i in range(len(local_weights)):
            target_weights[i] = self.tau * local_weights[i] + (
                        1 - self.tau) * target_weights[i]
        self.target_network.set_weights(target_weights)

    def update_epsilon(self):
        if self.epsilon >= self.epsilon_minimum:
            self.epsilon *= self.epsilon_decay

    def select_action(self, state):

        if self.epsilon > np.random.uniform():
            action = self.env.action_space.sample()
        else:
            action = np.argmax(
                self.local_network.predict(np.array([state])))

        return action

    def step(self, env, state):

        action = self.select_action(state)
        new_state, reward, done, _ = env.step(action)

        return action, reward, done, new_state

    def save(self):
        save_dir = os.path.join(os.getcwd(),
                                self.env.spec.id + "_" + datetime.datetime.now().strftime(
                                    '%Y-%m-%d_%H-%M-%S'))
        os.makedirs(save_dir)
        self.target_network.save("target_network.h5")
        self.local_network.save("local_network.h5")
        print("Weights saved successfully")

    def load(self):
        self.target_network.load_weights(
            "CartPole-v0_weights/target_network.h5")
        self.local_network.load_weights(
            "CartPole-v0_weights/local_network.h5")
        print("Weights loaded successfully")

    def print_info(self):
        print('\nTarget network')
        self.target_network.summary()
        print('\nLocal network')
        self.local_network.summary()
