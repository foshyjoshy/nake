from brain import Brains, BasicBrain, CrossoverBrainGenerator
from snake import Snake
from board import Board
from food import FoodGenerator

import consts
import time
import numpy as np
import matplotlib.pyplot as plt
import run


import h5py



if __name__ == "__main__":


    savedir = r"C:\Users\colyt\OneDrive\Documents\snake"
    board = Board.fromDims(10, 10)
    food = FoodGenerator(board, (1,1), 2321)
    snake = Snake.initializeAtPosition((5, 5), direction=consts.Moves.DOWN, name="loop")

    brain = BasicBrain.create(name="a")

    # brainPath = r"C:\Users\colyt\OneDrive\Documents\snake\brain.%04i.json"%(15)
    # with open(brainPath, "r") as FILE:
    #     di = json.load(FILE)
    #     brain = Brains.getInitialized(**di)
    #     weights = np.load(r"C:\Users\colyt\OneDrive\Documents\snake\weights.%04i.npz"%(15))
    #     brain.sequential_model.setWeights(weights)
    #     print ("brainPath", brainPath)


    brains = CrossoverBrainGenerator([brain, brain], n_generate=2)

    for brain in brains:
        snake = Snake.initializeAtPosition((5, 5), direction=consts.Moves.DOWN, name="loop")
        _food = food.duplicate()
        print (run.runSnake(snake, brain, _food, _food.board), snake.headPosition)



