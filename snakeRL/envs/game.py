from snakeRL.envs.game_state import GameState
from snakeRL.envs.render import Renderer
from snakeRL.envs.snake import Snake
from snakeRL.envs.items import Item

class GameRunner:

    def __init__(self, board_size=10, num_snakes=1, fruit_limit=1, render=False):
    
        self.game_state = GameState(board_size, num_snakes, fruit_limit)
        self.num_snakes= num_snakes
        self.isRender = render
        self.occupancy_grid = self.game_state.occupancy_grid
        if self.isRender:
            self.renderer = Renderer(board_size=board_size)
            self.renderer.step(self.game_state.occupancy_grid)
        

    def getStateForPolicy(self, snake_state):
        '''
        Get simplified version of state space in the form of simple integers
        '''
        if snake_state == 0: # state for dead snake
            return 0

        state_grid = []
        for i, item in enumerate(snake_state):
            if item == Item.BACKGROUND:
                state_grid.append(0)
            elif item == Item.FRUIT:
                state_grid.append(2)
            elif item == item.SNAKE:
                state_grid.append(1)
            elif item == item.SNAKE_HEAD:
                state_grid.append(3)
            elif item == item.MY_SNAKE:
                state_grid.append(4)
            elif item == item.MY_SNAKE_HEAD:
                state_grid.append(5)
        return state_grid
    def getAllSimplifiedSnakeStatesForPolicy(self):
        snake_states = self.game_state.snakeSpecificStates()
        states = []
        for s in snake_states:
            states.append(self.getStateForPolicy(s)) # create simplfied version of state for RL policy
        return states
        
    def step(self, actions=None):
        '''
        observation, reward, done, overall_board
        '''
        game_end = False # no more space on the grid for fruits, ideal scenario
        reward = [0]*self.num_snakes
        done = [False]*self.num_snakes
        # action is last action if no user input
        dead_snakes = []
        for i,s in enumerate(self.game_state.snake_store):
            if isinstance(s,Snake): # only for alive snakes
                action = actions[i]
                err, ate_fruit = s.updateState(action, self.game_state) # update snake position on board
                if err:
                    dead_snakes.append(i) # if snake collides with another snake then the other snake also dies
                    # keep info of dead snakes because some other snake might also collide. 
                elif ate_fruit:
                    # TODO: put reward specific for some snake
                    reward[i] = 1 # 1 for eating fruit
                    done[i] = False # snake is not killed

        # find if anything is killed or not, vanish if it is
        if len(dead_snakes) != 0:  
            for d in dead_snakes:
                self.game_state.snake_store[d] = 0 # remove all dead snakes from board
                reward[d] = 0 # populate reward and dead status of snake
                done[d] = True

        self.game_state.update() # updates occupancy grid with new snake positions and old fruit positions

        won = self.game_state.replinishFruits() # replinishes fruits in game board and fills in new fruits
        if won:
            # This means there is no more space in the grid and the game is won
            game_end = True

        # get snake specific states
        snake_states = self.game_state.snakeSpecificStates()
        states = []
        for s in snake_states:
            states.append(self.getStateForPolicy(s)) # create simplfied version of state for RL policy

        return self.game_state.occupancy_grid, states, reward, done, game_end
    
    def render(self):
        if self.isRender:
            self.renderer.step(self.game_state.occupancy_grid) # it needs the exact locations thaat have changed, snakes removed, snake added, fruit removed, fruit added
