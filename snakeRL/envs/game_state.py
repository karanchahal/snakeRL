from snakeRL.envs.items import Item
from snakeRL.envs.snake import Snake
import random

class GameState:
    
    def __init__(self, board_size=3, num_snakes=1, fruit_limit=1):
        self.board_size = board_size
        self.num_snakes = num_snakes
        self.total_fruit = 0
        self.fruit_limit = fruit_limit
        self.snake_store = []
        self.fruit_store = []
        self.occupancy_grid = [Item.BACKGROUND] * board_size*board_size # table of size n by n where n is board size
        self.snake_head = [0] * board_size*board_size

        self.initSnakes()
        self.replinishFruits()
    
    def initSnakes(self):
        for s in range(self.num_snakes):
            s = Snake(self.board_size, self)
            self.snake_store.append(s)
        
    def getFreeSpaces(self):
        indices = [i for i, x in enumerate(self.occupancy_grid) if x == Item.BACKGROUND]
        return indices

    def updateGrid(self, position, itemType): 
        # itemType: 1 for snake, 2 for fruit
        fruit = False
        dead = False
        
        if self.occupancy_grid[position] == Item.SNAKE:
            # snake exists in this position already so dead
            dead = True 
            return dead, fruit

        if itemType == Item.SNAKE and self.occupancy_grid[position] == Item.FRUIT:
            fruit = True
            # remove from fruit store list
            for i,pos in enumerate(self.fruit_store):
                if pos == position:
                    self.fruit_store = self.fruit_store[:i] + self.fruit_store[i+1:]
        return dead, fruit

    def replinishFruits(self):
        won = False
        if len(self.fruit_store) < self.fruit_limit:

            fruits_needed = self.fruit_limit - len(self.fruit_store)
            free_spaces = self.getFreeSpaces()

            if len(free_spaces) == 0:
                won = True 
                return won

            a = random.sample(range(len(free_spaces)), k=fruits_needed)
            listi = [free_spaces[i] for i in a]
            for i in listi:
                self.occupancy_grid[i] = Item.FRUIT # put fruit in this position
                self.fruit_store.append(i) # add to list of fruit locations
        return won

    def update(self):
        '''
        Builds game state from scratch by referring to the snakes store and fruit store
        Build one main state and several snake specific snake states for output observations
        '''
        self.occupancy_grid = [Item.BACKGROUND] * self.board_size*self.board_size # table of size n by n where n is board size
        self.snake_head = [0] * self.board_size*self.board_size
    

        # Building one main occupancy grid reference
        for s in self.snake_store:
            if isinstance(s,Snake):
                for i in s.position:
                    self.occupancy_grid[i] = Item.SNAKE
                self.snake_head[s.position[-1]] = Item.SNAKE_HEAD
        
        # Populating fruit in grid
        for i in self.fruit_store:
            self.occupancy_grid[i] = Item.FRUIT

    def snakeSpecificStates(self):
        # Building env according to the view of each snake for each agent

        snake_states = [0]*self.num_snakes
        for j, s in enumerate(self.snake_store):
            if isinstance(s,Snake):
                snake_state = self.occupancy_grid.copy()
                for i in s.position:
                    snake_state[i] = Item.MY_SNAKE
                snake_state[s.position[-1]] = Item.MY_SNAKE_HEAD
                snake_states[j] = snake_state

        return snake_states