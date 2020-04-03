from brain import Brains, BasicBrain
from snake import Snake
from board import Board
from food import FoodGenerator

import consts
import time
import numpy as np
import matplotlib.pyplot as plt
import os
import multiprocessing
import json

import run

import logging


import run


def runSnake(snake, brain, food, board, savedir=None, length=2):

    while snake.length < board.size:

        #Running brain

        #print (snake, board, food)

        move = consts.Moves(brain.computeMove(snake, board, food))




        snake.move(move)




        if food.isAvailable():
            if np.all(snake.headPosition == food.pos):
                snake.feed()
                food.findNext(snake)

                # if snake.length >= length:
                #
                #
                #     dirname = 'C:\\Users\\colyt\\OneDrive\\Documents\\snake'
                #     path = os.path.join(dirname, 'snake.{:04d}.png'.format(length))
                #
                #
                #     weightspath = os.path.join(savedir, "weights.%04i.npz"%(length))
                #     jsonpath = os.path.join(savedir, "brain.%04i.json"%(length))
                #
                #     with open(jsonpath, "w") as FILE:
                #         json.dump(brain.__getstate__(), FILE, indent=4, sort_keys=True)
                #
                #     np.savez(weightspath, **brain.sequential_model.getWeights())
                #
                #     im = snake.generatePreviewImage(board)
                #     im[food.pos[1], food.pos[0]] = 62
                #
                #     #fig = plt.Figure()
                #     plt.imshow(im, vmin=0)
                #     plt.title("{}".format(snake))
                #     plt.savefig(path)
                #     return snake.length

        if board.outside(snake.headPosition):
            break
        if snake.hasHeadCollidedWithBody():
            break
        if snake.unableToMove():
            break

        # im = snake.generatePreviewImage(board)
        # im[food.pos[1], food.pos[0]] = 66
        # plt.imshow(im, vmin=0)
        # plt.title("{}".format(snake))
        # plt.show()


    # with open(jsonpath, "w") as FILE:
    #     json.dump(brain.__getstate__(), FILE,  indent=4, sort_keys=True)
    #
    # np.savez(weightspath, brain.sequential_model.getWeights())
    #
    #
    # quit()
    return snake.length


if __name__ == "__main__":

    import pprint

    savedir = r"C:\Users\colyt\OneDrive\Documents\snake"
    board = Board.fromDims(10, 10)
    food = FoodGenerator(board, (1,1), 2321)
    snake = Snake.initializeAtPosition((5, 5), direction=consts.Moves.DOWN, name="loop")



    brainPath = r"C:\Users\colyt\OneDrive\Documents\snake\brain.%04i.json"%(15)
    with open(brainPath, "r") as FILE:
        di = json.load(FILE)
        brain = Brains.getInitialized(**di)
        weights = np.load(r"C:\Users\colyt\OneDrive\Documents\snake\weights.%04i.npz"%(15))
        brain.sequential_model.setWeights(weights)
        print ("brainPath", brainPath)


    food2 = food.duplicate()
    snake2 = Snake.initializeAtPosition((5, 5), direction=consts.Moves.DOWN, name=1, history=True)
    brain2 = brain.duplicate(name="brain%i"%(1), weights=True)
    runSnake(snake2, brain2, food2, food2.board)

    food3 = food.duplicate()
    snake3 = Snake.initializeAtPosition((5, 5), direction=consts.Moves.DOWN, name=2, history=True)
    brain3 = brain.duplicate(name="brain%i" % (2), weights=True)
    runSnake(snake3, brain3, food3, food3.board)

    print (snake2.history.arr)
    print(np.count_nonzero(snake2.history.arr == 4))
    print (snake2.history == snake3.history)




    print ("done")
    quit()
