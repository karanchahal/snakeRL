from snakeRL.envs.items import Item, Action
import random
import math

class Snake:

    def __init__(self, board_size, game_state):
        self.len = 1
        self.position = self.findRandomSpot(game_state)
        # adding snake
        game_state.occupancy_grid[self.position[-1]] = Item.SNAKE
        self.last_action = Action.UP
        self.board_size = board_size

    def findRandomSpot(self, game_state):
        # find random index in free spaces
        free_spaces = game_state.getFreeSpaces()
        a = random.sample(range(len(free_spaces)), k=1)
        return [free_spaces[i] for i in a]
    
    def getNewPosition(self, action):
        x,y = self.index2coordinates(self.position[-1])
       
        if action == Action.UP:
            x = x-1 
            if x < 0:
                return -1
        elif action  == Action.DOWN:
            x = x+1 
            if x > self.board_size-1:
                return -1
        elif action  == Action.LEFT:
            y = y-1 
            if y < 0:
                return -1
        elif action  == Action.RIGHT:
            y = y+1 
            if y > self.board_size-1:
                return -1
      
        return self.coordinates2index(x,y)

    def index2coordinates(self, i):
        
        i = i+1
        x = math.ceil(i/self.board_size)
        y = i % self.board_size

        if(y == 0):
            y = self.board_size
        if (x == 0):
            x = 1
        return x-1, y-1

    def coordinates2index(self, x, y):
        x = x+1
        y = y+1
        i = (x-1)*self.board_size + y

        return i-1

    def updateState(self, action, game_state):

        new_position = self.getNewPosition(action)
       
        err = False
        fruit_eaten = False
        if new_position == -1:
            # see if snake goes out of bounds
            err = True            
        else:
            dead, fruit_eaten = game_state.updateGrid(new_position, Item.SNAKE) # updates game board
            
            # if crashes into other snake
            if dead:
                err = True
            elif fruit_eaten:
                self.position.append(new_position)
            else:
                for i in range(len(self.position[:-1])):
                    self.position[i] = self.position[i+1]
                self.position[-1] = new_position   

        return err, fruit_eaten
        