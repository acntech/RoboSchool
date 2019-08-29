def play(agent, env):
    done = False
    agent.epsilon = 0
    total_reward = 0
    state = env.reset()

    while not done:
        action, reward, done, new_state = agent.step(env, state)
        state = new_state

        total_reward += reward

    print("Total Reward: {}".format(total_reward))