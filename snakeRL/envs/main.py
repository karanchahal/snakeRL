'''
CONFIG
'''
import random
import pygame 
import math
from items import Action
from game import GameRunner

game = GameRunner(board_size=3, num_snakes=1, fruit_limit=1)

# reward structure
# 0 every step
# 1 for fruit eaten 
# 100 for winning
# -100 for eating itself/ going out of bounds

while 1:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # print('LEFT')
                action = Action.LEFT
            if event.key == pygame.K_RIGHT:
                # print('RIGHT')
                action = Action.RIGHT
            if event.key == pygame.K_UP:
                # print('UP')
                action = Action.UP
            if event.key == pygame.K_DOWN:
                # print('DOWN')
                action = Action.DOWN

            grid, state, reward, won = game.step(actions=[action])
            print(state)
            print(reward)
            print(won)