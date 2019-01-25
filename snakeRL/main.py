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
        if new_position == -1:
            # see if snake goes out of bounds or crashes into another snake
            err = True            
        else:
            dead, fruit_eaten = game_state.updateGrid(new_position, Item.SNAKE) # updates game board
            
            if dead:
                err = True
            elif fruit_eaten:
                self.position.append(new_position)
            else:
                for i in range(len(self.position[:-1])):
                    self.position[i] = self.position[i+1]
                self.position[-1] = new_position   

        return err
        

class GameState:

    def __init__(self, board_size=3, num_snakes=1, fruit_limit=1):
        self.board_size = board_size
        self.num_snakes = num_snakes
        self.total_fruit = 0
        self.fruit_limit = fruit_limit
        self.snake_store = []
        self.fruit_store = []
        self.occupancy_grid = [Item.BACKGROUND] * board_size*board_size # table of size n by n where n is board size

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
            dead = True 
            return dead, fruit

        if itemType == Item.SNAKE and self.occupancy_grid[position] == Item.FRUIT:
            print('Eaten FRUIT !')
            fruit = True
            self.fruit_store = self.fruit_store[:-1]
        self.occupancy_grid[position] = itemType
        return dead, fruit

    def replinishFruits(self):
        if len(self.fruit_store) < self.fruit_limit:
            won = False

            fruits_needed = self.fruit_limit - len(self.fruit_store)
            free_spaces = self.getFreeSpaces()

            if free_spaces == 0:
                won = True 
                return won

            a = random.sample(range(len(free_spaces)), k=fruits_needed)
            listi = [free_spaces[i] for i in a]
            print(listi)
            for i in listi:
                self.updateGrid(i,Item.FRUIT)
                self.fruit_store.append(i)

            return won

    def update(self):

        self.occupancy_grid = [Item.BACKGROUND] * self.board_size*self.board_size # table of size n by n where n is board size

        for s in self.snake_store:
            for i in s.position:
                self.occupancy_grid[i] = Item.SNAKE
        
        for i in self.fruit_store:
            self.occupancy_grid[i] = Item.FRUIT

class GameRunner:

    def __init__(self, board_size=10, num_snakes=1, fruit_limit=1):
    
        self.game_state = GameState(board_size, num_snakes, fruit_limit)
        self.renderer = Renderer(board_size=board_size)
        self.renderer.step(self.game_state.occupancy_grid)
        # init game state
        # init snakes and everything

    def step(self, render=True, actions=None):
        # action is last action if no user input
        dead_snakes = []
        for i,s in enumerate(self.game_state.snake_store):
            action = actions[i]
            err = s.updateState(action, self.game_state) # update snake position on board
            if err:
                print('DEAD')
                dead_snakes.append(i)
                continue

            # find if anything is killed or not, vanish if it is
        if len(dead_snakes) != 0:  
            for d in dead_snakes:
                self.game_state.snake_store[d] = 0
            self.game_state.snake_store = [s for s in self.game_state.snake_store if isinstance(s,Snake)]
        # randomly generate fruit if fruit limit has decreased
        won = self.game_state.replinishFruits()

        self.game_state.update()

        if render:
            self.renderer.step(self.game_state.occupancy_grid) # it needs the exact locations thaat have changed, snakes removed, snake added, fruit removed, fruit added

        return self.game_state.occupancy_grid

class Sprite:

    def __init__(self, itemType, scale):
        self.itemType = itemType
        self.scale = scale
        self.surface = pygame.Surface((self.scale,self.scale))

        self.fillColor()
    
    def fillColor(self):
        if(self.itemType == Item.SNAKE):
            self.surface.fill((255,0,0))
        elif(self.itemType == Item.FRUIT):
            self.surface.fill((0,0,255))

class Renderer:

    def __init__(self, board_size, scale=30):

        self.board_size = board_size
        self.scale = scale
        
        self.initSurfaces()
        pygame.init()
    
    def initSurfaces(self):

        self.screen = pygame.display.set_mode((self.board_size*self.scale, self.board_size*self.scale))
        self.background =  pygame.Surface(self.screen.get_size())
        self.background.fill((0,255,0))
        self.screen.blit(self.background, (0, 0))

        pygame.display.update()

    def index2coordinates(self, i):
        
        i = i+1
        # print(i)
        x = math.ceil(i/self.board_size)
        y = i % self.board_size

        if(y == 0):
            y = self.board_size
        if (x == 0):
            x = 1
        # print(x,y)
        return x-1, y-1

    def step(self, new_grid):

        # case when snake eats a background comes after snake has moved from position
        # put snake in buffer and put background at that position
        for i in range(len(new_grid)):
            item = new_grid[i]
            x,y = self.index2coordinates(i)
            x = x*self.scale
            y = y*self.scale

            if item == Item.BACKGROUND:
                # print('background')
                self.screen.blit(self.background, (y,x))
            elif item == Item.FRUIT:
                # print('fruit')
                fruit = Sprite(itemType=Item.FRUIT, scale=self.scale)
                self.screen.blit(fruit.surface, (y,x))
            elif item == Item.SNAKE:
                # print('snake')
                snake = Sprite(itemType=Item.SNAKE, scale=self.scale)
                self.screen.blit(snake.surface, (y,x))

        pygame.display.update()


game = GameRunner(board_size=3, num_snakes=1, fruit_limit=1)

# reward structure
# -1 every step
# 1 for fruit eaten 
# 100 for winning
# -100 for eating itself/ going out of bounds

while 1:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # print('LEFT')
                action = Action.LEFT
                grid = game.step(actions=[action])
            if event.key == pygame.K_RIGHT:
                # print('RIGHT')
                action = Action.RIGHT
                grid = game.step(actions=[action])
            if event.key == pygame.K_UP:
                # print('UP')
                action = Action.UP
                grid = game.step(actions=[action])
            if event.key == pygame.K_DOWN:
                # print('DOWN')
                action = Action.DOWN
                grid = game.step(actions=[action])