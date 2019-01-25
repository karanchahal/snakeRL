import gym
from gym import error, spaces, utils
from gym.utils import seeding
from snakeRL.envs.game import GameRunner
from snakeRL.envs.items import Action
import numpy as np

class SnakeEnv(gym.Env):
    def __init__(self):
        
        self.occupancy_grid = []
        self.board_size = 3
        self.num_snakes = 1
        self.fruit_limit = 1

        self.game = GameRunner(board_size=self.board_size, num_snakes=self.num_snakes, fruit_limit=self.fruit_limit, render=True)
        
        self.occupancy_grid = self.game.occupancy_grid
        self.state = []
        self.reward = 0
        self.done = 0

        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=1,high=3, shape=(self.board_size*self.board_size,))

    def step(self, action):

        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))

        if action == 0:
            action = Action.UP
        elif action == 1:
            action = Action.DOWN
        elif action == 2:
            action = Action.LEFT
        elif action == 3:
            action = Action.RIGHT

        _, state, reward, done = self.game.step(actions=[action])

        self.state = state
        self.done = done 
        self.reward = reward

        return np.array(self.state,dtype=np.float32), self.reward, self.done, {}

    def reset(self):

        self.occupancy_grid = []
        self.board_size = 3
        self.num_snakes = 1
        self.fruit_limit = 1

        self.game = GameRunner(board_size=self.board_size, num_snakes=self.num_snakes, fruit_limit=self.fruit_limit, render=True)

        self.state = self.game.getStateForPolicy()
        self.reward = 0
        self.done = 0

        return np.array(self.state,dtype=np.float32)


    def render(self, mode='human', close=False):
        self.game.render()