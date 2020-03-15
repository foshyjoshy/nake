import numpy as np
import matplotlib.pyplot as plt
from snake import Snake
from utils import checkRequiredKeys, arrShapeMatch
from board import Board

import time
import copy


class RandomIndexGenerator():
    """ A simple wrapper around np.random.RandomState """

    SEED = "seed"
    COUNT = "count"

    def __init__(self, seed=None, count=0):
        if seed is None:
            seed = self.generateRandomSeed()
        self._set(seed, count)

    def _set(self, seed, count=0):
        """ Sets the seed and advances to count position"""
        self._seed = seed
        self._randomState = np.random.RandomState(seed=seed)
        if count > 0:
            # Skipping x number of random samples so its set to the correct state
            self._randomState.random_sample(count)
        self._count = count

    def __call__(self, *args):
        return self.get(*args)

    @staticmethod
    def generateRandomSeed():
        """ Generates random seed between 0-(2**32-1) """
        return np.random.randint(0, 2 ** 32 - 1, dtype=np.uint32)

    def duplicate(self, initialState=False):
        """ Duplicate class at current state if not initialState """
        count = [self._count, 0][initialState]
        return self.__class__(self._seed, count=count)

    def _get(self, size=1):
        """ returns a value or values between 0-1 """
        val = self._randomState.random_sample(int(size))
        self._count += 1
        return val

    def get(self, max_index):
        """ returns random index between 0 amd max_index"""
        return int(self._get() * (max_index / 1.))

    def __getstate__(self):
        """  """
        return {
            self.SEED: self._seed,
            self.COUNT: self._count,
        }

    def __setstate__(self, state):
        """ """
        checkRequiredKeys(state, [self.SEED, self.COUNT])
        self._set(state[self.SEED], state[self.COUNT])



class FoodGenerator():
    """ Handles the snakes food random state"""

    def __init__(self, board, pos, indexGenerator=None):
        if indexGenerator is None:
            indexGenerator = RandomIndexGenerator()

        assert isinstance(board, Board)
        assert isinstance(indexGenerator, RandomIndexGenerator)
        self._indexGenerator = indexGenerator

        self._initialPos = np.array(pos)
        self._initialPos.flags.writeable = False

        self.board = board
        self._arr = np.zeros([self.size], dtype=np.bool)
        self._status = True
        self._count = 0

        # Checking if our point is inside the board.
        if not self.board.inside(pos):
            raise Exception("Starting food position is outside board")

        self._pos = np.array(pos, dtype=int)
        self._pos.flags.writeable = False

    def __str__(self):
        return "FG {} count {} status {}".format(self.pos, self.count, self.status)

    def __array__(self):
        return self.pos

    @property
    def pos(self):
        """ Returns the pos"""
        return self._pos

    def copy(self, keepBoard=True):
        """ Returns a copy of this class """
        cls = copy.deepcopy(self)
        if keepBoard:
            cls.board = self.board
        return cls

    def duplicate(self, keepBoard=True, initialState=False):
        """ Returns a copy of this class """
        if keepBoard:
            board = self.board
        else:
            board = copy.deepcopy(self.board)
        return self.__class__(
            board,
            copy.deepcopy(self._initialPos),
            indexGenerator=self._indexGenerator.duplicate(initialState=initialState)
        )

    @property
    def shape(self):
        return self.board.shape

    @property
    def size(self):
        return self.board.size

    def isAvailable(self):
        """ """
        return self._status

    def notAvailable(self):
        """ """
        return self._status == False

    def _setpos(self, pos):
        """ Sets the new position of the food """
        self._pos.flags.writeable = True
        self._pos[:] = pos
        self._pos.flags.writeable = False
        self._count += 1

    def findNext(self, positions):
        """ Finds the next available position """
        if isinstance(positions, Snake):
            positions = positions.positions

        indexes = np.ravel_multi_index(positions.T[::-1], self.shape)

        self._arr[:] = True
        self._arr[indexes] = False

        #plt.imshow(self._arr.reshape(self.shape))
        #plt.show()

        available_indexes = np.nonzero(self._arr)[0]
        if available_indexes.size:
            # If we have enough space for next position
            ridx = self._indexGenerator(available_indexes.shape[0])
            self._setpos(np.unravel_index(available_indexes[ridx], self.shape)[::-1])
        else:
            # We are unable to find any available space for food.
            self._setpos((-1, -1))
            self._status = False

        return self.pos


if __name__ == "__main__":

    import consts

    board = Board.fromDims(12, 6)
    food = FoodGenerator(board, (2, 2))
    snake = Snake.initializeAtPosition((10, 5), direction=consts.Moves.DOWN)

    im = snake.generatePreviewImage(board, color_body=10, color_head=26)

    a = time.time()

    for i in range(10000):
        if np.all(snake.headPosition == food.pos):
            print("error")
        food.findNext(snake)
        im[food.pos[1], food.pos[0]] += 1
        # plt.show()

    food2 = food.duplicate()
    print(food2.findNext(snake))
    print(food.findNext(snake))
    print(food._count)
    quit()

    print(time.time() - a)
    plt.imshow(im, vmin=0)
    plt.colorbar()
    plt.show()
