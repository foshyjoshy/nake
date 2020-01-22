import numpy as np

DTYPE_SNAKE = np.int32

STR_UP = "up"
STR_DOWN = "down"
STR_LEFT = "left"
STR_RIGHT = "right"

MOVE_STR = [STR_UP, STR_DOWN, STR_LEFT, STR_RIGHT]



MOVE_UP = np.array([0, -1], dtype=DTYPE_SNAKE)
MOVE_DOWN = np.array([0, 1], dtype=DTYPE_SNAKE)
MOVE_LEFT = np.array([-1, 0], dtype=DTYPE_SNAKE)
MOVE_RIGHT = np.array([1, 0], dtype=DTYPE_SNAKE)


MOVEMENTS = {
    STR_UP : MOVE_UP,
    STR_DOWN : MOVE_DOWN,
    STR_LEFT : MOVE_LEFT,
    STR_RIGHT : MOVE_RIGHT
}

VALID_MOVEMENTS = {
    STR_UP  : [STR_UP, STR_LEFT, STR_RIGHT],
    STR_DOWN : [STR_DOWN, STR_LEFT, STR_RIGHT],
    STR_LEFT : [STR_DOWN, STR_UP, STR_LEFT],
    STR_RIGHT : [STR_DOWN, STR_UP, STR_RIGHT],
}

PI2 = np.pi*2

ANGLES_45 = range(0, 361, 45)