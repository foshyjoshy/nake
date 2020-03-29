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



def runSnake(snake, brain, food, board, savedir=None):

    while snake.length < board.size:

        #Running brain

        #print (snake, board, food)

        moveIdx = brain.computeMove(snake, board, food)
        snake.move(consts.Moves(moveIdx))

        if food.isAvailable():
            if np.all(snake.headPosition == food.pos):
                snake.feed()
                food.findNext(snake)

                if snake.length > 8:
                    im = snake.generatePreviewImage(board)
                    im[food.pos[1], food.pos[0]] = 62
                    plt.imshow(im, vmin=0)
                    plt.title("{}".format(snake))
                    plt.savefig(path)
                    print (snake, food._indexGenerator._count)
                    quit()


                # dirname = 'C:\\Users\\colyt\\OneDrive\\Documents\\snake'
                # path = os.path.join(dirname, 'snake.{:08d}.png'.format(loop))
                #
                # if snake.length > 9:
                #
                #     weightspath = os.path.join(savedir, "weights.npz")
                #     jsonpath = os.path.join(savedir, "brain.json")
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
                #     print (snake, food._indexGenerator._count)
                #     quit()

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
    food = FoodGenerator(board, (1, 1), 2321)
    snake = Snake.initializeAtPosition((5, 5), direction=consts.Moves.DOWN, name="loop")

    brainPath = r"C:\Users\colyt\OneDrive\Documents\snake\brain.json"
    with open(brainPath, "r") as FILE:
        di = json.load(FILE)
        pprint.pprint(di)
        brain = Brains.getInitialized(**di)
        weights = np.load(r"C:\Users\colyt\OneDrive\Documents\snake\weights.npz")
        brain.sequential_model.setWeights(weights)

    mlength = 0
    loop=0
    while True:
        loop+=1

        food2 = food.duplicate()
        snake2 = Snake.initializeAtPosition((5, 5), direction=consts.Moves.DOWN, name=loop)
        brain2 = brain.duplicate(name="brain%i"%(loop), weights=True)
        brain2.mutate(5)

        mlength = max(mlength, runSnake(snake2, brain2, food2, food2.board, savedir=savedir))
        if loop % 1000 == 1:
            print ("Loop", loop, mlength)

