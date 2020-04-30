from snake import Snake
from brain import BrainBase
from food import FoodGenerator
from board import Board
from consts import Moves, Terminated
import numpy as np
from snakeio import Writer


def runSnake(snake, brain, foodGenerator, board=None, callback_move=None, callback_finished=None):
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
    """ Run a brain generator """

    # Creating writer to save output
    writer = Writer(output_path)
    # Writing input food generator
    writer.write_food(input_food_generator, name="input_foodGenerator")
    # Writing input snake
    writer.write_snake(input_snake, name="input_snake")

    for brain in brain_generator:
        brain_name = writer.write_brain(brain)
        snake = input_snake.duplicate()
        food_generator = input_food_generator.duplicate(initialState=True)
        term = runSnake(snake, brain, food_generator)

    if close_file:
        writer.close()

    return writer.filename
