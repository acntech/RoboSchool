import numpy as np
import random
from collections import deque, namedtuple
import threading

class ExperienceReplay:

    def __init__(self, parameters):
        self.buffer_size = parameters["buffer_size"]
        self.batch_size = parameters["batch_size"]
        self.experience_buffer = deque(maxlen=self.buffer_size)

        self.experience = namedtuple("Experience",
                                     field_names=["state", "action",
                                                  "reward", "done",
                                                  "new_state"])
        self.experience_lock = threading.Lock()

    def add_experience(self, state, action, reward, done, new_state):
        e = self.experience(state, action, reward, done, new_state)
        self.experience_buffer.append(e)

    def get_batch(self):

        self.experience_lock.acquire()
        try:
            if len(self.experience_buffer) < self.batch_size:
                experiences = self.experience_buffer
            else:
                experiences = random.sample(self.experience_buffer,
                                            self.batch_size)
        finally:
            self.experience_lock.release()

        states = np.vstack(
            [e.state for e in experiences if e is not None])
        actions = np.vstack(
            [e.action for e in experiences if e is not None])
        rewards = np.vstack(
            [e.reward for e in experiences if e is not None])
        new_states = np.vstack(
            [e.new_state for e in experiences if e is not None])
        dones = np.vstack(
            [e.done for e in experiences if e is not None])

        return (states, actions, rewards, dones, new_states)

    def warm_up(self, env):
        for _ in range(10):
            state = env.reset()
            done = False

            while not done:
                action = env.action_space.sample()
                new_state, reward, done, _ = env.step(action)
                self.add_experience(state, action, reward, done, new_state)
                state = new_state
