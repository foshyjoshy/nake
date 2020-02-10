import numpy as np
import matplotlib.pyplot as plt
from snake import Snake
import time

import random



class FoodGenerator():
    """ Handles the snakes food random state"""

    def __init__(self, board, pos=None, state=None, seed=None):
        self.randomState = np.random.RandomState(seed=seed)
        if state is not None:
            self.randomState.set_state(state)

        self.state = self.randomState.get_state()
        self.board = board
        self._arr = np.zeros([self.size], dtype=np.bool)

        # if pos is not None:
        #     self.pos = pos
        # else:
        #     self.findNext()
        #


    @property
    def shape(self):
        return self.board.shape

    @property
    def size(self):
        return self.board.size

    def findNext(self, positions):
        """ Finds the next available position """
        if isinstance(positions, Snake):
            positions = positions.positions

        indexes = np.ravel_multi_index(positions.T[::-1], self.shape)

        self._arr[:] = True
        self._arr[indexes] = False

        available_indexes = np.nonzero(self._arr)[0]
        ridx = random.randint(0, available_indexes.shape[0] - 1)

        # # Check if indexing is correct
        # c = self._arr.reshape(self.shape)
        # plt.imshow(c)
        # plt.show()

        return np.unravel_index(available_indexes[ridx], self.shape)



from board import Board
from snake import Snake
import consts

snake = Snake.initializeAtPosition((4,4), direction=consts.Moves.DOWN)
board = Board.fromDims(6, 6)
gen = FoodGenerator(board)

im = snake.generatePreviewImage(board)
for i in range(200):
    idx = gen.findNext(snake)
    im[idx]=66

plt.imshow(im, vmin=0)
plt.colorbar()
plt.show()

