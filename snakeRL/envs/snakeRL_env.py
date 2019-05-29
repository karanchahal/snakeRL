import gym
from gym import error, spaces, utils
from gym.utils import seeding
from snakeRL.envs.game import GameRunner
from snakeRL.envs.items import Action
import numpy as np

class SnakeEnv(gym.Env):
    def __init__(self):
        
        self.occupancy_grid = []
        self.board_size = 5
        self.num_snakes = 2
        self.fruit_limit = 2
        self.isRender = False

        self.game = GameRunner(board_size=self.board_size, num_snakes=self.num_snakes, fruit_limit=self.fruit_limit, render=self.isRender)
        
        self.occupancy_grid = self.game.occupancy_grid
        self.stateList = self.game.getAllSimplifiedSnakeStatesForPolicy()
        self.rewardList = [0]*self.num_snakes
        self.doneList = [False]*self.num_snakes

        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=1,high=5, shape=(self.board_size*self.board_size,))

    def step(self, actionList):

        # assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))

        formattedActionList = []
        for action in actionList:
            if action == 0:
                formattedActionList.append(Action.UP)
            elif action == 1:
                formattedActionList.append(Action.DOWN)
            elif action == 2:
                formattedActionList.append(Action.LEFT)
            elif action == 3:
                formattedActionList.append(Action.RIGHT)
        _, stateList, rewardList, doneList, game_end = self.game.step(actions=formattedActionList) # List of _, state, reward, done 

        self.stateList = stateList
        self.doneList = [True if b else a for a,b in zip(self.doneList, doneList)]
        self.rewardList = [a+b for a,b in zip(self.rewardList, rewardList)]

        return self.stateList, self.rewardList, self.doneList, {'game_end':game_end} # send state array

    def reset(self):

        self.occupancy_grid = []

        self.game = GameRunner(board_size=self.board_size, num_snakes=self.num_snakes, fruit_limit=self.fruit_limit, render=self.isRender)
        self.stateList = self.game.getAllSimplifiedSnakeStatesForPolicy()
        self.rewardList = [0]*self.num_snakes
        self.doneList = [False]*self.num_snakes

        return np.array(self.stateList,dtype=np.float32) # Todo send state array for multiple agents


    def render(self, mode='human', close=False):
        self.game.render()
