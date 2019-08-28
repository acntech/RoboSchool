import gym
import collections
from tensorboardX import SummaryWriter

ENV_NAME = "FrozenLake-v0"
GAMMA = 0.9
ALPHA = 0.2
TEST_EPISODES = 20


class QTableAgent:
    def __init__(self):
        self.env = gym.make(ENV_NAME)
        self.state = self.env.reset()
        self.values = collections.defaultdict(float)

    def sample_env(self):
        """
        This function obtains the next transition from the env.
        A random action is sampled from the action space.

        :return: old state, action , reward for this state-action and
        the new state
        """
        action = self.env.action_space.sample()
        old_sate = self.state
        new_state, reward, is_done, _ = self.env.step(action)
        self.state = self.env.reset() if is_done else new_state
        return (old_sate, action, reward, new_state)

    def best_value_and_action(self, state):
        """
        Finds the best action to take from this state by takeing the
        largest value we have in the values dict. If no value found,
        zero will be used

        This func is used twice:
         - In the test episode phase to evaluate our policy
         - In the value update phase
        :param state:
        :return:
            best value found
            best action found
        """
        best_value, best_action = None, None
        for action in range(self.env.action_space.n):
            action_value = self.values[(state, action)]
            if best_value is None or best_value < action_value:
                best_value = action_value
                best_action = action

        return best_value, best_action

    def value_update(self, s, a, r, next_s):
        """
        Values table updated using one step from the environment. We
        blend the previous and the new value of the state-action and
        perform the Bellman update
        :param s: state
        :param a: action
        :param r: reward
        :param next_s: the resulting new state
        """
        best_v, _ = self.best_value_and_action(next_s)
        new_val = r + GAMMA * best_v
        old_val = self.values[(s, a)]

        self.values[(s, a)] = old_val * (1-ALPHA) + new_val * ALPHA

    def play_episode(self, env):
        """
        Plays one full episode on a provided test environment. Every
        action is taken based on the current Q-values. This is used to
        evaluate our current progress
        :param env: environment to test our agent in
        :return: total reward for the episode
        """
        total_reward = 0.0
        state = env.reset()
        while True:
            _, action = self.best_value_and_action(state)
            new_state, reward, is_done, _ = env.step(action)
            total_reward += reward
            if is_done:
                break
            state = new_state
        return total_reward

    def print_Q(self):
        print(self.values)


if __name__ == "__main__":
    test_env = gym.make(ENV_NAME)
    agent = QTableAgent()
    writer = SummaryWriter(comment="-q-learning")

    iter_no = 0
    best_reward = 0.0
    while True:
        iter_no += 1
        s, a, r, next_s = agent.sample_env()
        agent.value_update(s, a, r, next_s)
        reward = 0.0

        for _ in range(TEST_EPISODES):
            reward += agent.play_episode(test_env)
        reward /= TEST_EPISODES

        writer.add_scalar("reward", reward, iter_no)

        if reward > best_reward:
            print("Best reward updated %.3f -> %.3f" % (best_reward, reward))
            best_reward = reward
        if reward > 0.80:
            print("Solved in %d iterations!" % iter_no)
            break
        i=input()

    writer.close()
