from statistics import mean
from src.features.utils import threadDoneCounter
import threading
import time
import gym

NUM_THREADS = 4
TIMEOUT = 40


def train(agent, iterations, episodes, log=False, record=False):

    env = agent.return_env()
    total_reward_list, iterations_list = [], []
    agent.experience_replay.warm_up(env)

    print(f'Starting to train with {NUM_THREADS} threads')

    for episode in range(episodes):

        t_counter = threadDoneCounter(NUM_THREADS)

        if (episode != 0):
            agent.update_epsilon()

        time_tag = time.time()

        # Start the training threads
        for thread_i in range(NUM_THREADS):
            t = threading.Thread(target=episode_thread,
                                 args=(agent,
                                       iterations,
                                       iterations_list,
                                       total_reward_list,
                                       time_tag,
                                       t_counter))
            # print(f'starting thread {t} in episode {episode} with {iterations} iterations')
            t.start()


        # Train on the generated experience while the threads are
        # generating experience data. Stop the learning when all
        # threads are finished. This is a thread join
        num_learn = 50
        while (not t_counter.is_done()) or (num_learn >= 0):
            agent.learn()
            agent.update_target_network()
            num_learn -= 1


        # train_thread = threading.current_thread()
        # print(train_thread)


        if episode % 10 == 0:
            test_reward = agent.test_play(record=False)

            print \
                ("Episode: {} | Average iterations: {} | Average total reward: {} | Epsilon: {} | Test reward: {}" \
                  .format(episode, mean(iterations_list), mean(total_reward_list), agent.epsilon, test_reward))

            total_reward_list.clear()
            iterations_list.clear()

            if log: agent.save()
            # if test_reward >= 200:
            #     print('The game is solved')

        if log:
            agent.write_tensorboad(episode,
                               mean(iterations_list),
                               mean(total_reward_list),
                               agent.epsilon)


def episode_thread(agent, iterations, iterations_list,
                   total_reward_list, time_tag, t_counter):

    env = gym.make(agent.env.spec.id)
    state = env.reset()
    total_reward = 0

    for iteration in range(iterations):

        # Race protected
        action, reward, done, new_state = agent.step(env, state)

        # Race protected
        agent.experience_replay.add_experience(state, action, reward,
                                               done, new_state)

        state = new_state

        total_reward += reward

        if done:
            break

        if TIMEOUT != None and (time.time() - time_tag) >= TIMEOUT:
            break

    total_reward_list.append(total_reward)
    iterations_list.append(iteration + 1)

    t_counter.increment()

