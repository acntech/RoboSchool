import os
import numpy as np
from pathlib import Path
from tensorboardX import SummaryWriter
import gym
import json

from src.features.utils import generate_timestamp
from src.models.DQN import QNetwork
from src.features.experience_buffer import ExperienceReplay
from src.features.utils import load_param_json

CURRENT_PATH = Path(__file__).resolve().parent
NN_STORAGE_PATH = CURRENT_PATH.joinpath('agent_storage')


class DQNAgent:

    def __init__(self, ENV_NAME):

        self.parameters = load_param_json(ENV_NAME)

        self.env = gym.make(ENV_NAME)
        self.test_env = gym.make(ENV_NAME)

        self.timestamp = generate_timestamp()
        self.agent_name = self.timestamp + "_" + self.env.spec.id
        self.agent_storage_path = NN_STORAGE_PATH.joinpath(self.agent_name)

        if not NN_STORAGE_PATH.exists():
            os.mkdir(NN_STORAGE_PATH)

        if not self.agent_storage_path.exists():
            os.mkdir(self.agent_storage_path)

        self.writer = SummaryWriter(logdir=self.agent_storage_path,
                                    comment='DQN-' + self.env.spec.id)

        self.local_network = QNetwork(self.env,
                                      self.parameters).build_q_dense_from_json()
        self.target_network = QNetwork(self.env,
                                       self.parameters).build_q_dense_from_json()

        self.experience_replay = ExperienceReplay(self.parameters)

        self.epsilon = self.parameters["epsilon_init"]
        self.epsilon_decay = self.parameters["epsilon_decay"]
        self.epsilon_minimum = self.parameters["epsilon_minimum"]
        self.tau = self.parameters["tau"]
        self.gamma = self.parameters["gamma"]
        self.epochs = self.parameters["epochs"]

    def return_env(self):
        return self.env

    def return_test_env(self):
        return self.test_env

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

        self.target_network.save(\
            self.agent_storage_path.joinpath("target_network.h5"))
        self.local_network.save(\
            self.agent_storage_path.joinpath("local_network.h5"))

        with open(self.agent_storage_path.joinpath('parameters.txt'), 'w') as param_file:
            json.dump(self.parameters, param_file)

    def load(self):

        self.target_network.load(\
            self.agent_storage_path.joinpath("target_network.h5"))
        self.local_network.load(\
            self.agent_storage_path.joinpath("local_network.h5"))

    def write_tensorboad(self,
                         episode,
                         mean_iterations,
                         mean_total_reward,
                         epsilon):

        self.writer.add_scalar("Mean iterations",
                               mean_iterations,
                               episode)
        self.writer.add_scalar("Mean Total Reward",
                               mean_total_reward,
                               episode)
        self.writer.add_scalar("Epsilon", epsilon, episode)

    def test_play(self, record=False):
        env = self.test_env

        if record:
            self.initialize_record()
            env = self.monitor

        done = False
        temp_epsilon = self.epsilon
        self.epsilon = 0
        total_reward = 0
        state = env.reset()

        while not done:
            action, reward, done, new_state = self.step(env,
                                                        state)
            state = new_state
            total_reward += reward

        self.epsilon = temp_epsilon

        return total_reward

    def start_record(self):
        self.record_dir_path = self.agent_storage_path.joinpath('videos')
        if not self.record_dir_path.exists():
            os.mkdir(self.record_dir_path)

        self.monitor = gym.wrappers.Monitor(self.test_env,
                                       directory=self.record_dir_path,
                                       force=True)


        # monitor.close()
        # env.close()
        #
        # HTML("""
        # <video width="640" height="480" controls>
        #   <source src="{}" type="video/mp4">
        # </video>
        # #
        # """.format("./videos/" + list(
        #     filter(lambda s: s.endswith(".mp4"),
        #            os.listdir("./videos/")))[-1]))

    def print_networks(self):
        print('\nTarget network')
        self.target_network.summary()
        print('\nLocal network')
        self.local_network.summary()
