from brain import Brains, BasicBrain, CrossoverBrainGenerator, BasicBrainGenerator
from snake import Snake, SnakeActions
from board import Board
from food import FoodGenerator
from layers import Layer

import consts
import time
import numpy as np
import matplotlib.pyplot as plt
import run


import h5py



#TODO Get food per movement from history
#TODO Save term
#TODO Get fitness from these above


def callback_move(snake, board):
    im = snake.generatePreviewImage(board)
    plt.imshow(im, vmax=255)
    plt.show()

if __name__ == "__main__":

    foodGenerator = FoodGenerator(Board.fromDims(10, 10), (1, 1), 2321)
    snake = Snake.initializeAtPosition(
        (5,5),
        direction=consts.Moves.DOWN,
        name="loop",
        history=True,
        length=4
    )

    #path = r"C:\tmp\brain_snake.npz"
    #snake2 = Snake.load(path)


    for brain in BasicBrainGenerator(n_generate=100000):
        sn = snake.duplicate()

        fo = foodGenerator.duplicate(initialState=True)
        term = run.runSnake(sn,brain,fo)
        s =  (sn.history.movesPerFood())
        if s is not None:
            print (s)

        path = r"C:\tmp\brain_snake.npz"
        sn.save(path, compressed=True)
        #if term == consts.Terminated.UNABLE_TO_MOVE:
        # if sn.length == 5:
        #     fo = foodGenerator.duplicate(initialState=True)
        #     print (sn)
        #     snake2 = sn.load(path)
        #     print (sn==snake2)
        #     print(snake2)
        #     sn = snake.duplicate()
        #     term = run.runSnake(sn, brain, fo, callback_move=callback_move)
        #
        #     print(term)
        #     print(sn)
        #     #im = sn.generatePreviewImage(fo.board)
        #     #plt.imshow(im, vmax=255)
        #     #plt.show()
        #     quit()

