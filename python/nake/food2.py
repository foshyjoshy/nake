import numpy as np
import matplotlib.pyplot as plt
from snake import Snake
import time

import random



class FoodGenerator():
    """ Handles the snakes food random state"""

    def __init__(self, board, pos, state=None, seed=None):
        self.randomState = np.random.RandomState(seed=seed)
        if state is not None:
            self.randomState.set_state(state)

        # Need to store so we are able to duplicate class
        self._initialPos = np.array(pos)
        self._initialState = self.randomState.get_state()

        self.board = board
        self._arr = np.zeros([self.size], dtype=np.bool)
        self.count = 0

        # Checking if our point is inside the board.
        if not self.board.pointInside(pos):
            raise Exception("Starting food position is outside board")
        self.pos = np.array(pos, dtype=int)

    def __str__(self):
        return "FG2 {} count {}".format(self.pos,self.count)

    # def __array__(self):
    #     return self.pos

    @property
    def shape(self):
        return self.board.shape

    @property
    def size(self):
        return self.board.size

    def duplicateInitialRandomSeed(self):
        """ Returns a duplicated random state from the initial seed"""
        rstate = np.random.RandomState()
        rstate.set_state(self._initialState)
        return rstate

    def duplicateCurrentRandomSeed(self):
        """ Returns a duplicated random state from the current seed """
        rstate = np.random.RandomState()
        rstate.set_state(self.randomState.get_state())
        return rstate


    def findNext(self, positions):
        """ Finds the next available position """
        if isinstance(positions, Snake):
            positions = positions.positions

        indexes = np.ravel_multi_index(positions.T[::-1], self.shape)

        self._arr[:] = True
        self._arr[indexes] = False

        available_indexes = np.nonzero(self._arr)[0]
        ridx = self.randomState.randint(0, available_indexes.shape[0])

        self.pos[:] = np.unravel_index(available_indexes[ridx], self.shape)
        self.count+=1





from board import Board
from snake import Snake
import consts

snake = Snake.initializeAtPosition((4,4), direction=consts.Moves.DOWN)
board = Board.fromDims(6,6)
food = FoodGenerator(board, (2,2))

im = snake.generatePreviewImage(board)
a = time.time()
for i in range(100):
    food.findNext(snake)
    print (food)
    im[food.pos[0], food.pos[1]]=66

print (time.time()-a)
plt.imshow(im, vmin=0)
plt.colorbar()
plt.show()

