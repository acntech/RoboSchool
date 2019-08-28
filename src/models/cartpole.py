import gym

env = gym.make("CartPole-v0")

env.reset()
done = False
while not done:
    _, _, done, _ = env.step(env.action_space.sample())
    #env.render()

env.close()

print('Succsessful!!!!')