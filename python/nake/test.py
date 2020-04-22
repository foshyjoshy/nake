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



if __name__ == "__main__":

    board = Board.fromDims(10, 10)
    foodGenerator = FoodGenerator(board, (1, 1), 2321)

    for brain in BasicBrainGenerator(n_generate=20):
        food = foodGenerator.duplicate(initialState=True)
        snake = Snake.initializeAtPosition((5, 5), direction=consts.Moves.DOWN, name="loop", history=False)

        term = run.runSnake(snake, brain, foodGenerator, board)
        print (term)

