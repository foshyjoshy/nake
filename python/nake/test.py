from brain import Brain
from snake import Snake
from board import Board
from food2 import FoodGenerator


import consts

import time
import numpy as np
import matplotlib.pyplot as plt

brain = Brain()
snake = Snake.initializeAtPosition((5,5), direction=consts.Moves.DOWN)
board = Board.fromDims(10, 10)
food = FoodGenerator(board, (1,1))



input_arr = np.zeros([14])
input_arr[:] = -1


a = time.time()
for i in range(10):
    snake.moves2BoardEdges(board, moves=input_arr[:4])
    input_arr[4:6] = food.pos - snake.headPosition
    print (input_arr[4:6], food, snake.headPosition)
    snake.moves2Self(moves=input_arr[6:14])


    moveIdx = brain.compute(input_arr[..., None])
    snake.move(consts.Moves(moveIdx))

    #TODO CHECK SNAKES NEW POSITION




    print(input_arr)
    im = snake.generatePreviewImage(board)
    im[food.pos[1], food.pos[0]] = 127
    plt.imshow(im, vmin=0)
    plt.show()

    print(snake.headPosition, consts.Moves(moveIdx))



print (time.time()-a)

