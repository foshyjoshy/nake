from brain import Brain
from snake import Snake
from board import Board

import time

snake = Snake.initializeAtPosition((31,6), brain=Brain())
board = Board(64, 64)

#10,000 in 1.6 on laptop

a = time.time()
for i in range(1000):
    snake.computeMove(board, (50,50))
    print (snake)
    #quit()

print (time.time()-a)

