from statistics import mean


def train(agent, env, iterations, episodes):

    total_reward = 0
    total_reward_list, iterations_list = [], []
    agent.experience_replay.warm_up(env)

    for episode in range(episodes):

        state = env.reset()
        total_reward = 0

        if (episode != 0):
            agent.update_epsilon()

        for iteration in range(iterations):

            action, reward, done, new_state = agent.step(env, state)
            agent.experience_replay.add_experience(state, action, reward, done, new_state)

            state = new_state

            agent.learn()
            agent.update_target_network()
            total_reward += reward

            if done:
                break

        total_reward_list.append(total_reward)
        iterations_list.append(iteration +1)

        if episode % 10 == 0:
            print \
                ("Episode: {} | Average iterations: {} | Average total reward: {} | Epsilon: {} " \
                  .format(episode, mean(iterations_list), mean(total_reward_list), agent.epsilon))
            total_reward_list.clear()
            iterations_list.clear()