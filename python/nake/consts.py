import numpy as np
from enum import Enum

DTYPE_SNAKE = np.int32
PI2 = np.pi*2
ANGLES_45 = range(0, 361, 45)

class Moves(bytes, Enum):

    def __new__(cls, arr):
        value = len(cls.__members__)
        obj = bytes.__new__(cls, [value])
        obj._value_ = value
        obj.arr = arr
        return obj

    UP = np.array([ 0,-1], dtype=DTYPE_SNAKE)
    DOWN = np.array([ 0, 1], dtype=DTYPE_SNAKE)
    LEFT = np.array([-1, 0], dtype=DTYPE_SNAKE)
    RIGHT = np.array([ 1, 0], dtype=DTYPE_SNAKE)



