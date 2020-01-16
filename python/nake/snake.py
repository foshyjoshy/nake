import numpy as np
import consts
from exceptions import InvalidDirection,InvalidMove
from logging import debug


class Snake():

    POS_DTYPE = np.uint16

    def __init__(self, headIdx, length, direction, positions):
        if not positions.dtype == self.POS_DTYPE:
            TypeError('{} dtype arr expected'.format(self.POS_DTYPE))

        self.headIdx = headIdx
        self.length = length
        self.direction = direction
        self._positions = positions

        self.updatePositionalView()


    @classmethod
    def initializeAtPosition(cls, position, direction=consts.STR_DOWN, length=6):
        """ Starts from (x,y) moving in direction with length"""

        _positions = np.ones([max(length*2, 64), 2], dtype=cls.POS_DTYPE)*-1
        _positions[-length:] = position

        if direction.lower() == consts.STR_UP:
            _positions[-length:, 1]+=np.arange(length, dtype=cls.POS_DTYPE)
        elif direction.lower() == consts.STR_DOWN:
            _positions[-length, 1]-=np.arange(length, dtype=cls.POS_DTYPE)
        elif direction.lower() == consts.STR_LEFT:
            _positions[-length, 0] += np.arange(length, dtype=cls.POS_DTYPE)
        elif direction.lower() == consts.STR_RIGHT:
            _positions[-length, 0] -= np.arange(length, dtype=cls.POS_DTYPE)
        else:
            raise Exception("{} it not a valid direction... using one of {}".format(direction, consts.DISTANCES_STR))

        return cls(_positions.shape[0]-length, length, direction, _positions)


    def updatePositionalView(self):
        """ Updates the positional arr view"""
        self.positions = self._positions[self.headIdx:self.headIdx+self.length]


    def expand(self, n=None):
        """ Expands the position arr by n values"""
        if n is None: n = self._positions.shape[0]
        debug("Expanding position by {}".format(n))
        self._positions = np.vstack([self._positions,
                np.zeros([n, 2], dtype=self._positions.dtype)])
        self.updatePositionalView()

    def hasHeadCollidedWithBody(self):
        """Returns if the current head position has collided with its body"""
        return np.any(np.all(self.positions[0] == self.positions[1:], axis=1))

    def feed(self, updateArrView=True):
        """ Feeds snake a piece of fruit"""
        self.length += 1
        if updateArrView:
            self.updatePositionalView()

    def move(self, direction=None, feed=False):
        """ Moves snake along this direction"""
        if direction is None:
            direction = self.direction
        ''' #Removing checks for speed
        else:
            if direction not in consts.MOVEMENTS:
                raise InvalidDirection(direction)
            if direction not in consts.VALID_MOVEMENTS[self.direction]:
                raise InvalidMove(direction, consts.VALID_MOVEMENTS[self.direction])
        '''
        if self.length*2 > self._positions.shape[0]:
            self.expand()

        if self.headIdx == 0:
            # Resetting snake position
            self._positions[-self.length:] = self._positions[:self.length]
            self.headIdx = self._positions.shape[0]-self.length

        self.headIdx -= 1
        self._positions[self.headIdx] = self._positions[self.headIdx+1]+consts.MOVEMENTS[direction]

        # Check if we need increase the snake length
        if feed:
            self.feed(updateArrView=False)

        # Update view to stay in sync
        self.updatePositionalView()


    def moveUp(self, **kwargs):
        """ Moves the snake up"""
        return self.move(consts.STR_UP, **kwargs)

    def moveDown(self, **kwargs):
        """ Moves the snake down"""
        return self.move(consts.STR_DOWN, **kwargs)

    def moveLeft(self, **kwargs):
        """ Moves the snake left"""
        return self.move(consts.STR_LEFT, **kwargs)

    def moveRight(self, **kwargs):
        """ Moves the snake right"""
        return self.move(consts.STR_RIGHT, **kwargs)





import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import time
snake = Snake.initializeAtPosition((10,10), direction=consts.STR_UP, length=4)
a = time.time()
for i in range(10000):
    snake.moveLeft(feed=False)
    snake.moveRight(feed=False)
    if snake.hasHeadCollidedWithBody():
        print ("Collided")
        quit()
    #quit()
print (time.time()-a)
print (snake.length)







