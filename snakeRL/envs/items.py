from enum import Enum

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
