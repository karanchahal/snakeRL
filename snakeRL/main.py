'''
CONFIG
'''
import random
from enum import Enum
import pygame 
import math

class Item(Enum):
    BACKGROUND = 0
    SNAKE = 1
    FRUIT = 2

class Action(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Color(Enum):
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)

class Snake:

    def __init(self, game_state):
        self.len = 1
        self.position = [self.findRandomSpot(game_state)]
        self.last_action = Action.UP

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
        self.occupancy_grid = [Item.BACKGROUND] * board_size*board_size # table of size n by n where n is board size

        self.initSnakes()
        self.initFruits()
    
    def initSnakes(self):
        for s in self.num_snakes:
            s = Snake(self)
            self.snake_store.append(s)
        
    def getFreeSpaces(self):
        indices = [i for i, x in enumerate(self.occcupancy_grid) if x == Item.BACKGROUND]
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
                self.updateGrid(i,Item.FRUIT)

    def update(self):
        for s in self.snake_store:
            for i in s.position:
                self.occupancy_grid[i] = Item.SNAKE

class GameRunner:

    def __init__(self, board_size=10, num_snakes=1, fruit_limit=1):
    
        self.game_state = GameState(board_size, num_snakes, fruit_limit)
        self.renderer = Renderer(board_size, num_snakes, fruit_limit)
        # init game state
        # init snakes and everything

    def step(self, render=False, actions=None):
        # action is last action if no user input
        for i,s in enumerate(self.game_state.snake_store):
            action = actions[i]
            s.updateState(action) # update snake position on board
            self.game_state.update() # inform game of snake update on board
            # find if anything is killed or not, vanish if it is
        
        # randomly generate fruit if fruit limit has decreased
        self.game_state.replinishFruits()

        if render:
            self.renderer.step() # it needs the exact locations thaat have changed, snakes removed, snake added, fruit removed, fruit added

        return self.game_state.occupancy_grid

class Sprite:

    def __init__(self, itemType, scale):
        self.itemType = itemType
        self.scale = scale
        self.surface = pygame.Surface((self.scale,self.scale))
        self.pos = self.surface.get_rect(0,0)

        self.fillColor()
    
    def fillColor(self):
        if(self.itemType == Item.SNAKE):
            self.surface.fill(Color.RED)
        elif(self.itemType == Item.FRUIT):
            self.surface.fill(Color.BLUE)
    
    def move(x,y):
        self.pos = self.surface.move(x - self.pos.x, y - self.pos.y)


class Renderer:

    def __init__(self, board_size, num_snakes, scale=20, screen_size=20):

        self.scale = scale
        self.board_size = board_size
        self.num_snakes = num_snakes
        self.screen_size = screen_size
        
        self.initSurfaces()
    
    def initSurfaces(self):

        self.screen = pygame.display.set_mode((self.screen_size*self.scale, self.screen_size*self.scale))
        self.background =  pygame.Surface(self.screen.get_size())
        self.background.fill(Color.GREEN)
        self.screen.blit(self.background, (0, 0))

        pygame.display.update()

    def index2coordinates(self, i):
        
        i = i+1
        x = math.floor(i/self.board_size)
        y = i % self.board_size

        if(y == 0):
            y = self.board_size
        if (x == 0):
            x = 1
        return x-1, y-1



    def step(self, new_grid):

        # case when snake eats a background comes after snake has moved from position
        # put snake in buffer and put background at that position
        for i in range(len(new_grid)):
            item = new_grid[i]
            x,y = self.index2coordinates(i)
            if item == Item.BACKGROUND:
                self.screen.blit(self.background, (x,y), (x,y))
            elif item == Item.FRUIT:
                fruit = Sprite(itemType=Item.FRUIT)
                self.screen.blit(fruit.surface, (x,y), (x,y))
            elif item == Item.SNAKE:
                snake = Sprite(itemType=Item.SNAKE)
                self.screen.blit(snake.surface, (x,y), (x,y))

        pygame.display.update()


    
    



# def render(grid):

def getAction():
    action = input()

    if(action == 'w'):
        action = Action.UP
    elif(action == 'a'):
        action = Action.LEFT
    elif(action == 's'):
        action = Action.DOWN
    elif(action == 'd'):
        action = Action.RIGHT
    return action

# keep surfaces for snake
# one background
# surfaces for fruits


surface_grid = [0]*
def render(grid):

pygame.init() 


game = GameRunner(board_size=10, num_snakes=1, fruit_limit=1)
for i in range(1000):
    action = getAction()
    grid = game.step([action])
    render(grid)