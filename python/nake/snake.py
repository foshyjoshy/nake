import numpy as np
import consts
from logging import debug
import utils
from enum import IntEnum

class SnakeActions(IntEnum):
    """ Enum to store all available snake actions"""
    MOVE_UP = 0
    MOVE_DOWN = 1
    MOVE_LEFT = 2
    MOVE_RIGHT = 3
    EAT = 4

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_



class SnakeHistory():
    """ Simple way to store snake history and check snake movement history """

    HISTORY = "history"
    DEFAULT_LENGTH = 10

    MOVES_TO_ACTION = {
        consts.Moves.UP: SnakeActions.MOVE_UP,
        consts.Moves.DOWN: SnakeActions.MOVE_DOWN,
        consts.Moves.LEFT: SnakeActions.MOVE_LEFT,
        consts.Moves.RIGHT: SnakeActions.MOVE_RIGHT,
    }

    def __init__(self, headIndex, historyArr):
        self._index = headIndex
        self._historyArr = historyArr

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            # raise Exception("{} is not instance {}".format(other, self.__class__))
            return False
        elif not other.arr.shape == self.arr.shape:
            return False
        else:
            return np.all(other.arr == self.arr)

    @classmethod
    def fromArrs(cls, historyArrr):
        """ creates class from a single history array """
        return cls(len(historyArrr), historyArrr)

    def getArrs(self):
        """ Returns this classes numpy arrays """
        return {self.HISTORY: self.arr}

    @classmethod
    def createEmpty(cls, length=None):
        """ Create an empty history object"""
        historyArray = np.zeros(cls.DEFAULT_LENGTH if length is None else length, dtype=np.int32)
        return cls(0, historyArray)

    @property
    def arr(self):
        """ returns history array view"""
        return self._historyArr[:self._index]

    @property
    def size(self):
        """ Returns the size of the history stack"""
        return self._index

    def getIndexesForAction(self, action):
        """ returns the indexes for given action """
        if not SnakeActions.has_value(action):
            raise Exception('"{}" is not a valid action'.format(action))
        return np.where(self.arr == action)[0]

    def movesPerFood(self):
        """ returns the mean moves taken to find food"""
        indexes = self.getIndexesForAction(SnakeActions.EAT)
        if not len(indexes):
            return None
        return (indexes[-1]-indexes.shape[0]+1)/indexes.shape[0]

    def moves_made(self):
        """ Returns the number of moves made"""
        return np.sum(np.any([
            self.arr == SnakeActions.MOVE_UP,
            self.arr == SnakeActions.MOVE_DOWN,
            self.arr == SnakeActions.MOVE_LEFT,
            self.arr == SnakeActions.MOVE_RIGHT], axis=0))

    def expand(self, n=None):
        """ Expands historyArr arr by n values"""
        if n is None: n = self._historyArr.shape[0]
        debug("Expanding history by {}".format(n))
        self._historyArr = np.hstack([self._historyArr,
                                      np.zeros([n], dtype=self._historyArr.dtype)])

    def add(self, value):
        """ add to history"""
        if self._index == self._historyArr.shape[0]:
            self.expand()
        self._historyArr[self._index] = value
        self._index += 1

    def addMove(self, move):
        """ Add move history stack """
        self.add(self.MOVES_TO_ACTION[move])

    def addEat(self):
        """ Add eat action history stack"""
        self.add(SnakeActions.EAT)

    def toActions(self):
        """ Turns numpy arr into SnakeActions """
        return map(SnakeActions, self._historyArr)

    def duplicate(self):
        """ Returns a copy of the current class"""
        return self.__class__(int(self._index), self._historyArr.copy())


class Snake():
    """ Snake class """

    MOVES_REMAINING = "moves_remaining"
    NAME = "name"
    DIRECTION = "direction"
    HISTORY = "history"
    POSITIONS = "positions"
    STATE = "state"

    DEFAULT_MOVES = 28

    def __init__(self, headIdx, length, direction,
                 positions, movesRemaining=None, name=None, history=None):

        if movesRemaining is None:
            movesRemaining = int(self.DEFAULT_MOVES)
        if not positions.dtype == consts.DTYPE_SNAKE:
            TypeError('{} dtype arr expected'.format(consts.DTYPE_SNAKE))

        self.headIdx = headIdx
        self.length = length
        self.direction = direction
        self._positions = positions
        self.movesRemaining = movesRemaining
        self.name = name or ""
        self.history = history

        self.updatePositionalView()

    def __str__(self):
        return "Snake name:{} headPos:{} direction:{} length:{} remaining moves:{}" \
            .format(self.name, self.headPosition, self.direction, self.length, self.movesRemaining)

    def __len__(self):
        return self.length

    def __eq__(self, other):

        # Checking positions first
        if not isinstance(other, self.__class__):
            return False
        elif not other.positions.shape == self.positions.shape:
            return False
        elif not np.all(other.positions == self.positions):
            return False
        # Direction
        elif not self.direction == other.direction:
            return False
        # Moves remaining is the same
        elif not self.movesRemaining == other.movesRemaining:
            return False
        # Checks if we have history and its the same
        elif not self.history == other.history:
            return False
        else:
            return True

    @classmethod
    def initializeAtPosition(cls, position, direction=consts.Moves.DOWN, length=4, history=False, **kwargs):
        """ Starts from (x,y) moving in direction with length"""

        _positions = np.ones([max(length * 2 + 1, 64), 2], dtype=consts.DTYPE_SNAKE) * -1
        _positions[-length:] = position

        if direction == consts.Moves.UP:
            _positions[-length:, 1] += np.arange(length, dtype=consts.DTYPE_SNAKE)
        elif direction == consts.Moves.DOWN:
            _positions[-length:, 1] -= np.arange(length, dtype=consts.DTYPE_SNAKE)
        elif direction == consts.Moves.LEFT:
            _positions[-length:, 0] += np.arange(length, dtype=consts.DTYPE_SNAKE)
        elif direction == consts.Moves.RIGHT:
            _positions[-length:, 0] -= np.arange(length, dtype=consts.DTYPE_SNAKE)
        else:
            raise Exception("{} it not a valid direction... using one of {}".format(direction, consts.Moves))

        if history:
            history = SnakeHistory.createEmpty()
        else:
            history = None

        return cls(_positions.shape[0] - length, length, direction, _positions, history=history, **kwargs)

    def set_empty_history(self):
        """ Sets empty snake history """
        self.history = SnakeHistory.createEmpty()

    def duplicate(self, name=None, duplicate_history=True):
        """ Duplicates snake """
        if duplicate_history and self.history is not None:
            history = self.history.duplicate()
        else:
            history = None

        return self.__class__(
            int(self.headIdx),
            int(self.length),
            self.direction,
            self._positions.copy(),
            movesRemaining=int(self.movesRemaining),
            name=name or self.name,
            history=history,
        )

    @property
    def arr(self):
        """ Makes call a little easier"""
        return self.positions

    @property
    def headPosition(self):
        """ Returns the current head position """
        return self.positions[0]  # TODO Maybe faster to store head view in arr

    @property
    def bodyPositions(self):
        """ Returns a view of the body positions"""
        return self.positions[1:]

    def canMove(self):
        """ Returns if the snake is able to move """
        return self.movesRemaining > 0

    def unableToMove(self):
        """ Returns if the snake is unable to move"""
        return self.canMove() == False

    def updatePositionalView(self):
        """ Updates the positional arr view"""
        self.positions = self._positions[self.headIdx:self.headIdx + self.length]

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

    def movesPerFood(self):
        """ returns the mean moves taken to find food"""
        if self.history is not None:
            return self.history.movesPerFood()

    def feed(self, updateArrView=True, increaseMovesBy=None):
        """ Feeds snake a piece of fruit"""
        self.length += 1
        if updateArrView:
            self.updatePositionalView()
        self.movesRemaining += increaseMovesBy or self.DEFAULT_MOVES

        if self.history is not None:
            self.history.addEat()

    def move(self, direction=None, feed=False):
        """ Moves snake along this direction"""
        if direction is None:
            direction = self.direction

        if self.length * 2 > self._positions.shape[0]:
            self.expand()

        if self.headIdx == 0:
            # Resetting snake position
            self._positions[-self.length:] = self._positions[:self.length]
            self.headIdx = self._positions.shape[0] - self.length

        self.headIdx -= 1
        self._positions[self.headIdx] = self._positions[self.headIdx + 1] + direction.arr
        self.direction = direction

        # Adding move to history
        if self.history is not None:
            self.history.addMove(self.direction)

        # Check if we need increase the snake length
        if feed:
            self.feed(updateArrView=False)

        # Update view to stay in sync
        self.updatePositionalView()
        # Update our remaining moves
        self.movesRemaining -= 1
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

    def moves2Self(self, moves=None, default_value=None):
        """ Returns the number of moves to itself in 45% increments """
        return utils.moves2Body(
            self.headPosition, self.bodyPositions, consts.ANGLES_45, moves=moves, default_value=default_value)

    def generatePreviewImage(self, board, color_head=180, color_body=100, color_board=0, dtype=np.uint8):
        """ Simple view of the snake"""
        min_value = np.iinfo(dtype).min
        max_value = np.iinfo(dtype).max
        assert (color_head >= min_value and color_head <= max_value)
        assert (color_body >= min_value and color_body <= max_value)
        assert (color_board >= min_value and color_board <= max_value)

        im = np.zeros([board.height, board.width], dtype=dtype)
        im[:, :] = color_board

        body_pos = self.bodyPositions + [board.x, board.y]
        im[body_pos[:, 1], body_pos[:, 0]] = color_body

        # Drawing head position if inside board
        head_pos = [self.headPosition[0] + board.x, self.headPosition[1] + board.y]
        if board.inside(head_pos):
            im[head_pos[1], head_pos[0]] = color_head
        return im

    def save(self, filepath, compressed=False):
        """ Writes snake to npz """
        state = {
            self.MOVES_REMAINING: self.movesRemaining,
            self.NAME: self.name,
            self.DIRECTION: self.direction,
        }
        arrs = {
            self.POSITIONS: self.positions,
            self.STATE: state
        }
        if self.history is not None:
            arrs[self.HISTORY] = self.history.arr

        return (np.savez_compressed if compressed else np.savez)(filepath, **arrs)

    @classmethod
    def load(cls, filepath, name=None):
        """ Loads snake from npz path """
        npfile = np.load(filepath, allow_pickle=True)
        arrs = dict(npfile.items())
        state = arrs.pop(cls.STATE).item()
        if name is not None:
            state[cls.NAME] = name

        history = arrs.get(cls.HISTORY)
        if history is not None:
            history = SnakeHistory.fromArrs(history)

        positions = arrs[cls.POSITIONS]

        return cls(
            0,
            len(positions),
            state[cls.DIRECTION],
            positions,
            movesRemaining=state.get(cls.MOVES_REMAINING, int(cls.DEFAULT_MOVES)),
            name=name,
            history=history
        )



if __name__ == "__main__":
    from board import Board
    from food import FoodGenerator

    foodGenerator = FoodGenerator(Board.fromDims(10, 10), (1, 1), 2321)
    snake = Snake.initializeAtPosition(
        (5,5),
        direction=consts.Moves.DOWN,
        name="loop",
        history=True,
        length=4
    )


    import matplotlib.pyplot as plt
    a = snake.generatePreviewImage(foodGenerator.board)

    plt.imshow(a, vmin=0, vmax=255, cmap="gray")
    plt.show()



