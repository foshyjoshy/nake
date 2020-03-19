from brain import BasicBrain
from snake import Snake
from board import Board
from food import FoodGenerator

import consts
import time
import numpy as np
import matplotlib.pyplot as plt
import os
import multiprocessing




def runSnake(snake, brain, food, board):

    while snake.length < board.size:

        #Running brain
        moveIdx = brain.computeMove(snake, board, food)
        snake.move(consts.Moves(moveIdx))

        if food.isAvailable():
            if np.all(snake.headPosition == food.pos):
                snake.feed()
                food.findNext(snake)

                dirname = 'C:\\Users\\colyt\\OneDrive\\Documents\\snake'
                path = os.path.join(dirname, 'snake.{:08d}.png'.format(loop))

                if snake.length > 4:

                    im = snake.generatePreviewImage(board)
                    im[food.pos[1], food.pos[0]] = 62

                    #fig = plt.Figure()
                    plt.imshow(im, vmin=0)
                    plt.title("{}".format(snake))
                    plt.show()
                    #plt.savefig(path)
                    print (snake, food._indexGenerator._count)



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

    brain2 = BasicBrain.create(name="snake01")


    loop=0
    while True:
        loop+=1

        brain = BasicBrain.create(name="snake01")
        snake = Snake.initializeAtPosition((5, 5), direction=consts.Moves.DOWN, name=loop)
        food2 = food.duplicate()

        brain.sequential_model.setWeights(brain2.sequential_model.getWeights())




        runSnake(snake, brain, food2, food2.board)
        if loop % 10000 == 1:
            print ("Loop", loop)