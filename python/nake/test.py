from brain import Brain
from snake import Snake
from board import Board
from food2 import FoodGenerator

import consts
import time
import numpy as np
import matplotlib.pyplot as plt






def runSnake(snake, brain, food, board):

    while snake.length < board.size:

        # Getting inputs
        snake.moves2BoardEdges(board, moves=brain.input_arr[:4, 0])
        if food.isAvailable:
            brain.input_arr[4:6, 0] = food.pos - snake.headPosition
        else:
            brain.input_arr[4:6, 0] = 0
        snake.moves2Self(moves=brain.input_arr[6:14, 0])

        # Running brain
        moveIdx = brain.compute()
        snake.move(consts.Moves(moveIdx))

        if food.isAvailable():
            if np.all(snake.headPosition == food.pos):
                snake.feed()
                food.findNext(snake)

                if snake.length == 6:
                    print ("Found second food position")
                    # im = snake.generatePreviewImage(board)
                    # im[food.pos[1], food.pos[0]] = 127
                    # plt.imshow(im, vmin=0)
                    # plt.show()

        if board.outside(snake.headPosition):
            break
        if snake.hasHeadCollidedWithBody():
            break
        if snake.unableToMove():
            break

        # im = snake.generatePreviewImage(board)
        # im[food.pos[1], food.pos[0]] = 127
        # plt.imshow(im, vmin=0)
        # plt.show()

    #print(consts.Moves(moveIdx))


if __name__ == "__main__":

    board = Board.fromDims(10, 10)
    food = FoodGenerator(board, (1, 1))

    loop=0
    while True:
        loop+=1

        brain = Brain()
        snake = Snake.initializeAtPosition((5, 5), direction=consts.Moves.DOWN)
        food2 = food.getInitialStateCopy()

        runSnake(snake, brain, food2, food2.board)
        if loop % 100 == 1:

            print ("Loop", loop)