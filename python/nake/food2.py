import numpy as np
import matplotlib.pyplot as plt
from board import Board
import time

import random





class FoodGenerator():
    """ Handles the snakes food random state"""

    def __init__(self, board, pos=None, state=None, seed=None):
        self.randomState = np.random.RandomState(seed=seed)
        if state is None:
            self.randomState.set_state(state)

        self.state = self.randomState.get_state()
        self.board = board
        self._arr = np.zeros([self.size], dtype=np.bool)

    @property
    def shape(self):
        return self.board.shape

    @property
    def size(self):
        return self.board.size

    def findNext(self, positions):
        """ Finds the next available position """
        self._arr[:] = True
        self._arr[positions] = False
        #np.unravel_index

        indexes = np.nonzero(self._arr)[0]
        idx = random.randint(0, indexes.shape[0] - 1)


        y = int(index/board.width)
        x = index-(y*board.width)



gen = FoodGenerator()
gen.findNext()


a = time.time()

#randomState = random.seed(a=None)
for i in range(1000):
    random.randint(0, 1000)
print (time.time()-a)

a = time.time()

randomStateX = np.random.RandomState(seed=None)
for i in range(1000):
    randomStateX.randint(0, 1000)

print (time.time()-a)

quit()



board = Board.fromDims(128, 64)
numvalues = board.width*board.height

arr = np.zeros([numvalues], dtype=np.bool)
positions = np.arange(numvalues)
np.random.shuffle(positions)
positions = positions[:int(numvalues*0.8)]
print ("Snake length", positions.shape[0])



a = time.time()
for i in range(1000):
    arr[:] = True
    arr[positions] = False
    indexes = np.nonzero(arr)[0]
    index = random.randint(0, indexes.shape[0] - 1)
    #print (indexes)
    #break
    y = int(index/board.width)
    x = index-(y*board.width)

print (time.time()-a)


