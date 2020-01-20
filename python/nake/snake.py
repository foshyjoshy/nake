import numpy as np
import consts
from exceptions import InvalidDirection,InvalidMove
from logging import debug
from scipy.spatial.distance import cdist


class Snake():

    def __init__(self, headIdx, length, direction, positions):
        if not positions.dtype == consts.DTYPE_SNAKE:
            TypeError('{} dtype arr expected'.format(consts.DTYPE_SNAKE))

        self.headIdx = headIdx
        self.length = length
        self.direction = direction
        self._positions = positions

        self.updatePositionalView()


    @classmethod
    def initializeAtPosition(cls, position, direction=consts.STR_DOWN, length=6):
        """ Starts from (x,y) moving in direction with length"""

        _positions = np.ones([max(length*2+1, 64), 2], dtype=consts.DTYPE_SNAKE)*-1
        _positions[-length:] = position

        if direction.lower() == consts.STR_UP:
            _positions[-length:, 1]+=np.arange(length, dtype=consts.DTYPE_SNAKE)
        elif direction.lower() == consts.STR_DOWN:
            _positions[-length, 1]-=np.arange(length, dtype=consts.DTYPE_SNAKE)
        elif direction.lower() == consts.STR_LEFT:
            _positions[-length, 0] += np.arange(length, dtype=consts.DTYPE_SNAKE)
        elif direction.lower() == consts.STR_RIGHT:
            _positions[-length, 0] -= np.arange(length, dtype=consts.DTYPE_SNAKE)
        else:
            raise Exception("{} it not a valid direction... using one of {}".format(direction, consts.DISTANCES_STR))

        return cls(_positions.shape[0]-length, length, direction, _positions)


    @property
    def headPosition(self):
        """ Returns the current head position """
        return self.positions[0] #TODO Maybe faster to store head view in arr

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


    def getDistance2Self(self, angles, distances=None):
        """ Returns the distance to itself
            0 == Right
            90 == Down
            180 == Left
            270 == Up
        """
        if distances is None:
            distances = np.ones(len(angles))*-1

        # Getting angle
        diff =(self.positions[1:]-self.positions[0])#.astype(np.float32)
        ang = np.arctan2(diff[:,0], diff[:,1])
        val = np.rad2deg(ang % consts.PI2)
        #dist = cdist(self.positions[1:], self.positions[:1])
        dist = np.sqrt(diff[:,0]**2 + diff[:,1]**2)
        for idx, angle in enumerate(angles):
            idxs = np.where(val == angle)[0]
            if idxs.shape[0]:
                distances[idx] = np.min(dist[idxs])

        return distances


    def view(self, boardSize=[64, 64]):
        """ Simple view of the snake"""









import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import time
snake = Snake.initializeAtPosition((50,50), direction=consts.STR_UP, length=100)
a = time.time()
#for i in range(100):
snake.moveLeft(feed=True)
snake.moveLeft(feed=True)
#snake.moveLeft(feed=True)

#snake.moveDown(feed=True)
snake.moveDown(feed=True)
snake.moveDown(feed=True)
#snake.moveRight(feed=True)
snake.moveRight(feed=True)
snake.moveUp(feed=True)







print (consts.DTYPE_SNAKE)

#
self = snake
#
a = time.time()
diff = self.positions[1:]-self.positions[0]
#

distances = np.ones([8])*-1
for i in range(10000):
    diff = self.positions[1:] - self.positions[0]

    upIdx = np.where((diff[:,0]<=0) * (diff[:,0]==0))[0]
    if upIdx.shape[0]:
        distances[0] = np.max(diff[upIdx,1])*-1
    rightUpIdx = np.where((-diff[:,0]==diff[:,1]) * (diff[:,0] >= 0))[0]
    if rightUpIdx.shape[0]:
        distances[1] = np.min(diff[rightUpIdx, 1])*-1
    rightIdx = np.where((diff[:,0]>=0) * (diff[:,1]==0))[0]
    if rightIdx.shape[0]:
        distances[2] = np.min(diff[rightIdx, 0])
    rightDownIdx = np.where((diff[:,0]==diff[:,1]) * (diff[:,0] >= 0))[0]
    if rightDownIdx.shape[0]:
        distances[3] = np.min(diff[rightDownIdx, 0])
    downIdx = np.where((diff[:,0]==0) * (diff[:,1]>=0))[0]
    if downIdx.shape[0]:
       distances[4] = np.min(diff[downIdx, 1])
    leftDownIdx = np.where((diff[:,0]==-diff[:,1]) * (diff[:,0] <= 0))[0]
    if leftDownIdx.shape[0]:
       distances[5] = np.min(diff[leftDownIdx, 1])
    leftIdx = np.where((diff[:,0]<=0) * (diff[:,1]==0))[0]
    if leftIdx.shape[0]:
       distances[6] = np.max(diff[leftIdx, 0])*-1
    leftUpIdx = np.where((diff[:,0]==diff[:,1]) * (diff[:,0] <= 0))[0]
    if leftUpIdx.shape[0]:
       distances[7] = np.max(diff[leftUpIdx, 0])*-1

print (time.time()-a)
print (distances)
self = snake
#
a = time.time()
diff = self.positions[1:]-self.positions[0]
distances = np.ones([8])*-1
angles = range(0, 361, 45)
for i in range(10000):
    aa = self.getDistance2Self(angles, distances)
print (time.time()-a)
print (distances)
