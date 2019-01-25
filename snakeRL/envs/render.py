import pygame 
from snakeRL.envs.items import Item
import math

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