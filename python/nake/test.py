from brain import Brains, BasicBrain, CrossoverBrainGenerator, BasicBrainGenerator
from snake import Snake
from board import Board
from food import FoodGenerator
from layers import Layer

import consts
import time
import numpy as np
import matplotlib.pyplot as plt
import run


import h5py



#TODO SAVE SNAKE HISTORY/SNAKE
#TODO DUPLICATE SNAKE

#TODO Save history... for checking fitness
#TODO Save term
#TODO Get fitness from these above





if __name__ == "__main__":

    foodGenerator = FoodGenerator(Board.fromDims(10, 10), (1, 1), 2321)
    snake = Snake.initializeAtPosition((5, 5), direction=consts.Moves.DOWN, name="loop", history=False)


    for brain in BasicBrainGenerator(n_generate=20):
        sn = snake.duplicate()
        print (sn)
        fo = foodGenerator.duplicate(initialState=True)
        term = run.runSnake(sn,brain,fo)
        print(term)
        print(sn)
        im = sn.generatePreviewImage(fo.board)
        plt.imshow(im)
        plt.show()

        print (term)

