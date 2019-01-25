import gym 
import snakeRL 
import  time

env = gym.make('snakeRL-v0')
for i in range(100):
    env.reset()
    for _ in range(1000):
        state, reward, done = env.step(env.action_space.sample()) # take a random action
        # print('Reward: ', reward)
        # print('Done: ', done)

        if(done):
            break
