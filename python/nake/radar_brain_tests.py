from brain import RadarBrain
from snake import Snake, SnakeActions
from board import Board
from food import FoodGenerator
import consts
import matplotlib.pyplot as plt
import numpy as np
import utils
import time


# x = np.asarray([-1, 10, 20, 10,4], dtype=np.float64)
#
# np.mean(x) # calculates the mean of the array x
# x-np.mean(x) # this is euivalent to subtracting the mean of x from each value in x
# x-=np.mean(x) # the -= means can be read as x = x- np.mean(x)
#
# np.std(x) # this calcualtes the standard deviation of the array
# x/=np.std(x) # the /= means can be read as x = x/np.std(x)
# print (x)
#
# x = np.asarray([-1, 10, 20, 10,4], dtype=np.float64)
#
#
# #[-1.3653123   0.19910804  1.62130835  0.19910804 -0.65421214]
#
# from scipy import stats
# x =  stats.zscore(x)
#
# print ()
# print (x)
#
# quit()


board = Board.fromDims(31, 31)
food_generator = FoodGenerator(board, (20,20))


movesRemaining = 75
moves_increase_by = 60
snake = Snake.initializeAtPosition(
    (15, 19),
    direction=consts.Moves.DOWN,
    name="loop",
    history=True,
    length=19,
    movesRemaining=movesRemaining,
    moves_increase_by=movesRemaining,
)
for i in range(5):
    snake.move(consts.Moves.LEFT)
for i in range(2):
    snake.move(consts.Moves.DOWN)
for i in range(4):
    snake.move(consts.Moves.RIGHT)
#for i in range(2):
#    snake.move(consts.Moves.UP)

# snake = Snake.initializeAtPosition(
#     (15, 19),
#     direction=consts.Moves.DOWN,
#     name="loop",
#     history=True,
#     length=2,
#     movesRemaining=movesRemaining,
#     moves_increase_by=movesRemaining,
# )



brain = RadarBrain.create(name="sdddd")
brain.computeMove(snake, board, food_generator.pos)

