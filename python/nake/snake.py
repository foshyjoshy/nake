import numpy as np
import consts
from logging import debug
import utils


class Snake():


    def __init__(self, headIdx, length, direction,
                 positions, movesRemaining=200, name=None):
        if not positions.dtype == consts.DTYPE_SNAKE:
            TypeError('{} dtype arr expected'.format(consts.DTYPE_SNAKE))

        self.headIdx = headIdx
        self.length = length
        self.direction = direction
        self._positions = positions
        self.movesRemaining = movesRemaining
        self.name = name or ""

        self.updatePositionalView()


    def __str__(self):
        return "Snake name:{} headPos:{} direction:{} length:{} remaining moves:{}"\
            .format(self.name, self.headPosition, self.direction, self.length, self.movesRemaining)

    # def __array__(self):
    #     return self.bodyPositions

    @classmethod
    def initializeAtPosition(cls, position, direction=consts.Moves.DOWN, length=4, **kwargs):
        """ Starts from (x,y) moving in direction with length"""

        _positions = np.ones([max(length*2+1, 64), 2], dtype=consts.DTYPE_SNAKE)*-1
        _positions[-length:] = position

        if direction == consts.Moves.UP:
            _positions[-length:, 1]+=np.arange(length, dtype=consts.DTYPE_SNAKE)
        elif direction == consts.Moves.DOWN:
            _positions[-length:, 1]-=np.arange(length, dtype=consts.DTYPE_SNAKE)
        elif direction == consts.Moves.LEFT:
            _positions[-length:, 0] += np.arange(length, dtype=consts.DTYPE_SNAKE)
        elif direction == consts.Moves.RIGHT:
            _positions[-length:, 0] -= np.arange(length, dtype=consts.DTYPE_SNAKE)
        else:
            raise Exception("{} it not a valid direction... using one of {}".format(direction, consts.Moves))

        return cls(_positions.shape[0]-length, length, direction, _positions, **kwargs)


    @property
    def headPosition(self):
        """ Returns the current head position """
        return self.positions[0] #TODO Maybe faster to store head view in arr

    @property
    def bodyPositions(self):
        """ Returns a view of the body positions"""
        return self.positions[1:]


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

    def feed(self, updateArrView=True, increaseMovesBy=100):
        """ Feeds snake a piece of fruit"""
        self.length += 1
        if updateArrView:
            self.updatePositionalView()
        self.movesRemaining+=increaseMovesBy

    def move(self, direction=None, feed=False):
        """ Moves snake along this direction"""
        if direction is None:
            direction = self.direction

        if self.length*2 > self._positions.shape[0]:
            self.expand()

        if self.headIdx == 0:
            # Resetting snake position
            self._positions[-self.length:] = self._positions[:self.length]
            self.headIdx = self._positions.shape[0]-self.length

        self.headIdx -= 1
        self._positions[self.headIdx] = self._positions[self.headIdx+1]+direction.arr
        self.direction = direction

        # Check if we need increase the snake length
        if feed:
            self.feed(updateArrView=False)

        # Update view to stay in sync
        self.updatePositionalView()
        # Update our remaining moves
        self.movesRemaining-=1

        return True



    def moveUp(self, **kwargs):
        """ Moves the snake up"""
        return self.move(consts.Moves.UP, **kwargs)

    def moveDown(self, **kwargs):
        """ Moves the snake down"""
        return self.move(consts.Moves.DOWN, **kwargs)

    def moveLeft(self, **kwargs):
        """ Moves the snake left"""
        return self.move(consts.Moves.LEFT, **kwargs)

    def moveRight(self, **kwargs):
        """ Moves the snake right"""
        return self.move(consts.Moves.RIGHT, **kwargs)

    def moves2BoardEdges(self, board, moves=None):
        """ Returns the number moves to the four walls"""
        return board.movesToBoardEdges(self.headPosition, moves=moves)

    def moves2Self(self, moves=None):
        """ Returns the number of moves to itself in 45% increments """
        return utils.moves2Body(
            self.headPosition, self.bodyPositions, consts.ANGLES_45, moves=moves)

    def generatePreviewImage(self, board):
        """ Simple view of the snake"""
        im = np.zeros([board.height, board.width], dtype=np.uint8)
        im[:,:] = 0
        im[self.bodyPositions[:,1]+board.y, self.bodyPositions[:,0]+board.x] = 127
        im[self.headPosition[1]+board.y, self.headPosition[0]+board.x] = 255
        return im






if __name__ == "__main__":

    import matplotlib.pyplot as plt

    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)



    from board import Board
    board = Board.fromDims(10, 10)
    print (board)


    import time
    snake = Snake.initializeAtPosition((0,4), direction=consts.Moves.UP, length=6)




    a = time.time()
    snake.moveRight(feed=True)
    snake.moveRight(feed=True)
    snake.moveRight(feed=True)
    snake.moveRight(feed=True)
    snake.moveDown(feed=True)
    snake.moveDown(feed=True)
    snake.moveLeft()
    snake.moveLeft()
    snake.moveUp()
    print(snake)
    print (snake.moves2Self())
    print (snake.moves2BoardEdges(board))
    im= snake.generatePreviewImage(board)
    # plt.imshow(im, cmap="gray")
    # plt.show()
    #
    #
    # quit()



    snake.moveLeft(feed=True)
    snake.moveLeft(feed=True)
    snake.moveDown(feed=True)
    snake.moveDown(feed=True)
    snake.moveDown(feed=True)
    snake.moveRight(feed=True)
    snake.moveRight(feed=True)
    snake.moveUp(feed=True)
    print (snake)


    self = snake
    #
    a = time.time()
    diff = self.positions[1:]-self.positions[0]
    distances = np.ones([8])*-1
    for i in range(1000):
        self.moveLeft()
    print (time.time()-a)
    print (distances)
