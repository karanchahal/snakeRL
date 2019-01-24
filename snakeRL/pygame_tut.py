import sys, pygame

pygame.init()

size = width, height = 20, 20
scale = 20 # scale of each virtual pixel is 10 actual pixels = 1 virtual pixel

screen = pygame.display.set_mode((size[0]*scale, size[1]*scale))

background = pygame.Surface(screen.get_size())
background.fill((255, 255, 255))
screen.blit(background, (0, 0))
snake = pygame.Surface((1*scale,1*scale))
snake.fill((0,0,0))
screen.blit(snake, (0, 0))
last_pos = snake.get_rect()

while 1: 
    screen.blit(background, last_pos, last_pos)
    new_pos = last_pos.move(scale,scale)
    screen.blit(snake, new_pos)
    last_pos = new_pos
    pygame.display.update()