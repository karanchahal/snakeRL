import gym 
import snakeRL 
import  time

env = gym.make('snakeRL-v0')
for i in range(100):
    env.reset()
    for _ in range(1000):
        env.render()
        one = int(input("Action for snake 1"))
        two = int(input("Action for snake 2"))
        actionList = [one, two]

        states, rewards, dones, _ = env.step(actionList) # take a random action
        print(rewards)
        print(dones)
        # for i, agent in enumerate(outList):
        #     print(agent)
        #     state, reward, done,_ = agent
        #     if done:
        #         print("Agent i has died")

        # print('Reward: ', reward)
        # print('Done: ', done)
    

        # if(done):
        #     break
