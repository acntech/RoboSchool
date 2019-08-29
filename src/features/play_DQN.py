def play(agent):
    env = agent.return_test_env()
    done = False
    agent.epsilon = 0
    total_reward = 0
    state = env.reset()

    while not done:
        action, reward, done, new_state = agent.step(env, state)
        state = new_state

        total_reward += reward

    print("TEST: Total Reward: {}".format(total_reward))
