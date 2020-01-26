from brain import Brain
from snake import Snake
from board import Board
import consts

import time
import numpy as np
import matplotlib.pyplot as plt

brain = Brain()
snake = Snake.initializeAtPosition((5,5), direction=consts.Moves.DOWN)
board = Board.fromDims(10, 10)
foodPosition = (0,0)

input_arr = np.zeros([14])
input_arr[:] = -1


#plt.ion()

a = time.time()
for i in range(10):
    snake.moves2BoardEdges(board, moves=input_arr[:4])
    input_arr[4:6] = foodPosition - snake.headPosition
    print (input_arr[4:6], foodPosition, snake.headPosition)
    snake.moves2Self(moves=input_arr[6:14])

    print (input_arr)
    im= snake.generatePreviewImage(board)

    plt.imshow(im, cmap="gray")
    plt.show()

    moveIdx = brain.compute(input_arr[..., None])
    snake.move(consts.Moves(moveIdx))

    print(snake.headPosition, consts.Moves(moveIdx))



print (time.time()-a)

