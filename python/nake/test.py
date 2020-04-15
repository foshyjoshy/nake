from brain import Brains, BasicBrain, CrossoverBrainGenerator
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

    """
    brains = CrossoverBrainGenerator([brain, brain], n_generate=2)

    for brain in brains:
        snake = Snake.initializeAtPosition((5, 5), direction=consts.Moves.DOWN, name="loop")
        _food = food.duplicate()
        print (run.runSnake(snake, brain, _food, _food.board), snake.headPosition)
    """




    # All classes need to suport create_group from h5py
    # Make awesome IO class warpper for h5py

    # Save as we go. Keep ram low
    # 50,000 brains ... hdf5 500mb # 251.31146955 time taken
    # Time without saving ...64.91375851631
    # With running  but not saving ... 91.07679128646 ... This is first gen tho
    # Only store x number of the best brains. Store while running... maybe

    """
    h5f = h5py.File("mytestfile.hdf5", "w")
    grp = h5f.create_group("brains")
    brains = CrossoverBrainGenerator([brain, brain], n_generate=50000)
    for b in brains:
        braing = grp.create_group(b.name)
        for name, arr in b.getArrs().items():
            braing.create_dataset(name, data=arr)
    h5f.close()
    print ("TIMETAKEN", time.time()-st)
    """

    layer = Layer("dense", "input_layer", 10, 20)


    with h5py.File("test.hdf5", "w") as FILE:
        braing = FILE.create_group("ddddddd")
        braing.attrs["ddddd"] = "dfdfdf"
        braing.attrs["ddddsdsdsd"] = "sds"

        layer.add2h5py(braing)



        print (braing.keys())
        print (braing.attrs.keys())
        quit()



