import numpy as np
import consts
from exceptions import InvalidDirection,InvalidMove
from logging import debug



class Snake():

    POS_DTYPE = np.uint16

    def __init__(self, length, direction, positions):
        if not positions.dtype == self.POS_DTYPE:
            TypeError('{} dtype arr expected'.format(self.POS_DTYPE))
        self.length = length
        self.direction = direction
        self.positions = positions


    @classmethod
    def initializeAtPosition(cls, position, direction=consts.STR_DOWN, length=6):
        """ Starts from (x,y) moving in direction with length"""

        positions = np.ones([max(length*2, 64), 2], dtype=cls.POS_DTYPE)*-1
        positions[:length] = position

        if direction.lower() == consts.STR_UP:
            positions[1:length, 1]+=np.arange(1, length, dtype=cls.POS_DTYPE)
        elif direction.lower() == consts.STR_DOWN:
            positions[1:length, 1]-=np.arange(1, length, dtype=cls.POS_DTYPE)
        elif direction.lower() == consts.STR_LEFT:
            positions[1:length, 0] += np.arange(1, length, dtype=cls.POS_DTYPE)
        elif direction.lower() == consts.STR_RIGHT:
            positions[1:length, 0] -= np.arange(1, length, dtype=cls.POS_DTYPE)
        else:
            raise Exception("{} it not a valid direction... using one of {}".format(direction, consts.DISTANCES_STR))

        return cls(length, direction, positions)


    def expand(self, n=None):
        """ Expands the position arr by n values"""
        if n is None: n = self.positions
        debug("Expanding position by n {}".format(n))
        self.positions = np.vstack([self.positions,
                np.zeros([n, 2], dtype=self.positions.dtype)])


    def move(self, direction=None):
        """ Moves snake along this direction"""
        if direction is None:
            direction = self.direction
        else:
            if direction not in consts.MOVEMENTS:
                raise InvalidDirection(direction)
            if direction not in consts.VALID_MOVEMENTS[self.direction]:
                raise InvalidMove(direction, consts.VALID_MOVEMENTS[self.direction])

        if self.length == self.positions.shape[0]:
            self.expand()

        # Moving valid positions to the right by one
        self.positions[1:self.length+1] = self.positions[:self.length]
        self.positions[0]+= consts.MOVEMENTS[direction]


    def moveUp(self):
        """ Moves the snake up"""
        return self.move(consts.STR_UP)

    def moveDown(self):
        """ Moves the snake down"""
        return self.move(consts.STR_DOWN)

    def moveLeft(self):
        """ Moves the snake left"""
        return self.move(consts.STR_LEFT)

    def moveRight(self):
        """ Moves the snake right"""
        return self.move(consts.STR_RIGHT)










import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



import time
snake = Snake.initializeAtPosition((10,10), direction=consts.STR_UP)
a = time.time()
for i in range(100000):
    snake.moveUp()
print (snake.positions[:snake.length])
print (time.time()-a)













