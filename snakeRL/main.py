'''
CONFIG
'''
import random
from enum import Enum


class Item(Enum):
    SNAKE = 1
    FRUIT = 2

class Action(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Snake:

    def __init(self, game_state):
        self.len = 1
        self.position = [self.findRandomSpot(game_state)]
        self.last_action = 

    def findRandomSpot(game_state):
        # find random index in free spaces
        free_spaces = game_state.getFreeSpaces()
        i = random.sample(range(len(free_spaces)), k=1)
        return free_spaces[i]
    
    def updateState(new_position, game_state):
        err = False
        if self.game_state.invalidState(new_position):
            # see if snake goes out of bounds or crashes into another snake
            err = True            
        else:
            fruit_eaten = game_state.updateGrid(new_position) # updates game board

            if fruit_eaten:
                for i in range(len(self.position[:-1])):
                    self.position[i] = self.position[i+1]
                self.position[:-1] = new_position
            else:
                self.position.append(new_position)

        return err
        

class GameState:

    def __init__(self, board_size=10, num_snakes=1, fruit_limit=1):
        self.board_size = board_size
        self.num_snakes = num_snakes
        self.total_fruit = fruit_limit
        self.snake_store = []
        self.occupancy_grid = [0] * board_size*board_size # table of size n by n where n is board size

        self.initSnakes()
        self.initFruits()
    
    def initSnakes(self):
        for s in self.num_snakes:
            s = Snake(self)
            self.snake_store.append(s)
        
    def getFreeSpaces(self):
        indices = [i for i, x in enumerate(self.occcupancy_grid) if x == 0]
        return indices

    def updateGrid(self, position, itemType): 
        # itemType: 1 for snake, 2 for fruit
        fruit = False
        if itemType == 1 and self.occupancy_grid[position] == 2:
            fruit = True
            self.total_fruit -= itemType
        self.occupancy_grid[position] = itemType
        return fruit

    def replinishFruits(self):
        if self.total_fruit < self.fruit_limit:
            fruits_needed = self.total_fruit - self.fruit_limit
            free_spaces = self.getFreeSpaces()
            list_i = random.sample(range(len(free_spaces)), k=fruits_needed)
            for i in list_i:
                self.updateGrid(i,2)

    def update(self):
        for s in self.snake_store:
            for i in s.position:
                self.occupancy_grid[i] = 1

class GameRunner:

    def __init__(self):
        # init game state
        # init snakes and everything

    def step(self, actions):
        # action is last action if no user input
        for s in self.game_state.snake_store:
            action = actions[s]
            s.updateState(action) # update snake position on board
            self.game_state.update() # inform game of snake update on board
            # find if anything is killed or not , vanish if it is
        
        # randomly generate fruit if fruit limit has decreased
        self.game_state.replinishFruits()






    

CONFIG_NUM_SNAKES = 1
CONFIG_SIZE_BOARD = 50 # in cells

snakes = []
for i in range(CONFIG_NUM_SNAKES):
    # create snakes