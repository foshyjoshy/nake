import logging as LOG

from snake import Snake
from brain import Brains
from food import FoodGenerator
from board import Board





def runSnake(snake, brain, foodGenerator, board):
    """ Runs snake until it terminates"""

    assert isinstance(snake, Snake)
    assert isinstance(foodGenerator, FoodGenerator)
    assert isinstance(board, Board)









