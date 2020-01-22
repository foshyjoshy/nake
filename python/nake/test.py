from brain import Brain
from snake import Snake
from board import Board
import consts

import time
import numpy as np

brain = Brain()
snake = Snake.initializeAtPosition((31,6), direction=consts.STR_LEFT)
board = Board.fromDims(64, 64)
foodPosition = (10,10)

input_arr = np.zeros([14])
input_arr[:] = -1



a = time.time()
for i in range(5):
    #snake.getDistance2BoardEdges(board, distances=input_arr[:4])
    #input_arr[4:6] = foodPosition - snake.headPosition
    print (snake.getDistance2Self(distances=input_arr[5:14]))

    moveIdx = brain.compute(input_arr[..., None])
    snake.move(consts.MOVE_STR[moveIdx])

    print (consts.MOVE_STR[moveIdx])


print (time.time()-a)

