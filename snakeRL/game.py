from game_state import GameState
from render import Renderer
from snake import Snake
from enums import Item

class GameRunner:

    def __init__(self, board_size=10, num_snakes=1, fruit_limit=1):
    
        self.game_state = GameState(board_size, num_snakes, fruit_limit)
        self.renderer = Renderer(board_size=board_size)
        self.renderer.step(self.game_state.occupancy_grid)
        # init game state
        # init snakes and everything

    def getStateForPolicy(self):
        '''
        '''
        state_grid = []
        for i, item in enumerate(self.game_state.occupancy_grid):
            if item == Item.BACKGROUND:
                state_grid.append(0)
            elif item == Item.FRUIT:
                state_grid.append(1)
            elif item == item.SNAKE:
                if self.game_state.snake_head[i] == 1:
                    state_grid.append(3)
                else:
                    state_grid.append(2)
        return state_grid

    def step(self, render=True, actions=None):
        '''
        observation, reward, done, overall_board
        '''
        reward = 0
        # action is last action if no user input
        dead_snakes = []
        for i,s in enumerate(self.game_state.snake_store):
            action = actions[i]
            err, ate_fruit = s.updateState(action, self.game_state) # update snake position on board
            if err:
                dead_snakes.append(i)
                continue
            if ate_fruit:
                reward = 1

            # find if anything is killed or not, vanish if it is
        if len(dead_snakes) != 0:  
            for d in dead_snakes:
                self.game_state.snake_store[d] = 0
            self.game_state.snake_store = [s for s in self.game_state.snake_store if isinstance(s,Snake)]

        if len(self.game_state.snake_store) == 0: # for dead snake
            reward = -100
        
        # randomly generate fruit if fruit limit has decreased
        won = self.game_state.replinishFruits()
        if won:
            reward = 100

        self.game_state.update()

        if render:
            self.renderer.step(self.game_state.occupancy_grid) # it needs the exact locations thaat have changed, snakes removed, snake added, fruit removed, fruit added

        state = self.getStateForPolicy()

        return self.game_state.occupancy_grid, state, reward, won