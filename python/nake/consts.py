import numpy as np
from enum import Enum, IntEnum

DTYPE_SNAKE = np.int32
PI2 = np.pi*2
ANGLES_45 = range(0, 360, 45)

RADAR_ANGLES_BOUNDS_45 = range(0, 405, 45)


class Moves(bytes, Enum):

    def __new__(cls, arr):
        value = len(cls.__members__)
        obj = bytes.__new__(cls, [value])
        obj._value_ = value
        obj.arr = arr
        return obj

    def isOpposite(self, other):
        """ Checks if moves is the opposite direction """
        assert isinstance(other, Moves)
        return not np.any(other.arr+self.arr)


    UP = np.array([ 0,-1], dtype=DTYPE_SNAKE)
    DOWN = np.array([ 0, 1], dtype=DTYPE_SNAKE)
    LEFT = np.array([-1, 0], dtype=DTYPE_SNAKE)
    RIGHT = np.array([ 1, 0], dtype=DTYPE_SNAKE)



class Terminated(IntEnum):
    """ Stores how the snake was terminated"""

    UNABLE_TO_MOVE = "Unable to move"
    COLLIDED_WITH_BODY = "Collided with body"
    COLLIDED_WITH_EDGE = "Collided with edge"
    DIRECTION_REVERSED = "Direction reversed"

    def __new__(cls, text):
        value = len(cls.__members__)
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.text = text
        return obj

