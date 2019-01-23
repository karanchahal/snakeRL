# Setup

1. Create conda env
# Directives

1. Draw a board of variable size -arguments or config file
2. Then add number of snakes on board
3. Draw fruit on the board randomly but take care not to draw it on any occupied positions
4. snake size is 1 in the beginning
5. track size of it
6. state of snake is exact positions its body is in on the board
7. or maybe its a picture of the oard with the colour of playing snake coloured something else and toher snakes are coloured something else

8. conv features could capture state of game and snake in one go

9. not at each time step can take any action up down left right, or nothing. 

10. Action opposite the direction the snake is going to will be disregarded.

11. if snake colides with anytig non air or fruit, it dies. 

12. game ends if all snakes die

13. if snake eats a fruit, then at that  time step, the body will not move, simply head  moves one extra cell.

14. else if snake moves in air then, i states take value i+1 and head takes new value