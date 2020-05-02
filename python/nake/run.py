from snake import Snake
from brain import BrainBase
from food import FoodGenerator
from board import Board
from consts import Moves, Terminated

import numpy as np
from snakeio import Writer
import pandas as pd
from enum import Enum
from io import BytesIO

class Stats(str, Enum):
    """ Run stat enum"""

    TERM = ("term", np.int32)
    LENGTH = ("length", np.int32)
    MOVES_REMAINING = ("moves_remaining", np.int32)
    MOVES_MADE = ("moves_made", np.int32)
    MOVES_PER_FOOD = ("moves_per_food", np.float)
    DIRECTION = ("direction", np.int32)

    def __new__(cls, value, dtype):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.dtype = dtype
        return obj

    @classmethod
    def create_array(cls, n_values, default_value=-1):
        """ Creates an array with this number of values"""
        stats_dtypes = [(stat.value, stat.dtype) for stat in cls]
        arr = np.zeros([n_values], dtype=stats_dtypes)
        arr[:] = default_value
        return arr



def run_snake(snake, brain, foodGenerator, board=None, callback_move=None, callback_finished=None):
    """ Runs snake until it terminates"""
    if board is None:
        board = foodGenerator.board

    # Checking inputs
    assert isinstance(snake, Snake)
    assert isinstance(foodGenerator, FoodGenerator)
    assert isinstance(board, Board)
    assert isinstance(brain, BrainBase)

    term = None

    while snake.canMove():
        previous_move = snake.direction

        # Using brain to compute move
        move = Moves(brain.computeMove(snake, board, foodGenerator))
        # Moving snake
        snake.move(move)

        if callback_move is not None:
            callback_move(snake, board)

        if len(snake) > 1:
            # Checking if snake has moved back on itself
            if move.isOpposite(previous_move):
                term = Terminated.DIRECTION_REVERSED
                break

        if foodGenerator.isAvailable():
            # Feeding snake if food has been hit
            if np.all(snake.headPosition == foodGenerator.pos):
                snake.feed()
                foodGenerator.findNext(snake)

        # Check if snakes new position outside of board
        if board.outside(snake.headPosition):
            term = Terminated.COLLIDED_WITH_EDGE
            break
        # Check if snakes new position has collided with its own body
        if snake.hasHeadCollidedWithBody():
            term = Terminated.COLLIDED_WITH_BODY
            break

    else:
        term = Terminated.UNABLE_TO_MOVE

    if callback_finished is not None:
        callback_finished(snake, brain, foodGenerator, board)

    return term


def run_generator(brain_generator, input_snake, input_food_generator, output_path, close_file=True):
    """ Ru n a brain generator """

    # Making sure our snake has a history object for creating stats
    if input_snake.history is None:
        input_snake.set_empty_history()

    # Creating stat arr for storing info per brain
    stats = Stats.create_array(brain_generator.n_generate)
    brain_names = [None]*brain_generator.n_generate

    # Creating writer to save output
    writer = Writer(output_path)
    # Writing input food generator
    writer.write_food(input_food_generator, name="input_foodGenerator")
    # Writing input snake
    writer.write_snake(input_snake, name="input_snake")

    for bidx, brain in enumerate(brain_generator):
        brain_names[bidx] = writer.write_brain(brain)
        snake = input_snake.duplicate()
        food_generator = input_food_generator.duplicate(initialState=True)

        # Run snake
        stats[bidx][Stats.TERM] = run_snake(snake, brain, food_generator)

        # Add snake stats
        stats[bidx][Stats.MOVES_PER_FOOD] = snake.movesPerFood()
        stats[bidx][Stats.MOVES_REMAINING] = snake.movesRemaining
        stats[bidx][Stats.MOVES_MADE] = snake.history.moves_made()
        stats[bidx][Stats.LENGTH] = snake.length
        stats[bidx][Stats.DIRECTION] = snake.direction.value

    # Saving stats as pandas
    data_frame = pd.DataFrame(stats, columns=stats.dtype.names, index=brain_names)
    F = BytesIO()
    data_frame.to_excel(F, merge_cells=False)
    writer.zip.writestr("run_stats.xlsx", F.getbuffer())

    # Saving stats as npy
    F = BytesIO()
    np.savez(F, stats=stats, names=brain_names)
    writer.zip.writestr("run_stats.npz", F.getbuffer())


    if close_file:
        writer.close()

    return writer.filename
