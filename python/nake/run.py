from snake import Snake
from brain import BrainBase
from food import FoodGenerator
from board import Board
from consts import Moves, Terminated
from snakeio import Writer
from run_stats import RunStats, RunStatsStash


from time import perf_counter
from pprint import pprint

import numpy as np
import pandas as pd
from io import BytesIO



class BrainRunStash:
    """ Stashing brains via stats """

    DEFAULT_ORDER = [
        RunStats.LENGTH,
        RunStats.MOVES_MADE,
        RunStats.MOVES_PER_FOOD
    ]

    def __init__(self, max_brains=10, sort_order=None):
        self.stats = RunStatsStash(stash_size=max_brains, key_instance=BrainBase)
        self.sort_order = sort_order or self.DEFAULT_ORDER

    @property
    def brains(self):
        return self.keys

    def get_position(self, **kwargs):
        """ Based on the stats input it get the next index """
        currentStatus = self.stats.stats

    def add_brain(self, brain, **kwargs):
        """ adds a brain to the stash"""
        if self.stats.is_full():
            print ("ssss")
            quit()
        else:
            self.stats.append(brain, **kwargs)
            return True





def run_snake(snake, brain, foodGenerator, board=None, callback_move=None, callback_finished=None):
    """ Runs snake until it terminates"""
    if board is None:
        board = foodGenerator.board

    # Checking inputs
    assert isinstance(snake, Snake)
    assert isinstance(foodGenerator, FoodGenerator)
    assert isinstance(board, Board)
    assert isinstance(brain, BrainBase)

    while snake.canMove():
        previous_move = snake.direction

        # Using brain to compute move
        move = Moves(brain.computeMove(snake, board, foodGenerator))
        # Moving snake
        snake.move(move)

        if callback_move is not None:
            callback_move(snake, brain, board, foodGenerator.pos)

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
        callback_finished(term, snake, brain, foodGenerator, board)

    return {
        RunStats.TERM: term,
        RunStats.MOVES_REMAINING: snake.movesRemaining,
        RunStats.MOVES_MADE: snake.history.moves_made(),
        RunStats.LENGTH: snake.length,
        RunStats.DIRECTION: snake.direction.value,
    }





def run_generator(brain_generator, input_snake, input_food_generator, output_path, close_file=True, max_save=10):
    """ Ru n a brain generator """

    _time = perf_counter()
    _times = []

    # Making sure our snake has a history object for creating stats
    if input_snake.history is None:
        input_snake.set_empty_history()

    # Creating run stats object to save every brains performance
    stats_stash = RunStatsStash(brain_generator.n_generate)

    # Creating brain stash to save only x number of best brains
    brain_stash = BrainRunStash(max_brains=max_save)

    #_times.append(("Setup", perf_counter()-_time))

    brains = []
    for brain in brain_generator:
        # Duplicating inputs
        snake = input_snake.duplicate()
        food_generator = input_food_generator.duplicate(initialState=True)

        # Run snake
        run_stats = run_snake(snake, brain, food_generator)

        # Adding run stats into stat stash
        stats_stash.append(key=brain.name, **run_stats)

        # Adding brain to brain stash if performed well
        brain_stash.add_brain(brain=brain, **run_stats)


    quit()




    # # Creating writer to save output
    # writer = Writer(output_path)
    # # Writing input food generator
    # writer.write_food(input_food_generator, name="input_foodGenerator")
    # # Writing input snake
    # writer.write_snake(input_snake, name="input_snake")

    # import os
    # import psutil
    # process = psutil.Process(os.getpid())
    # print(process.memory_info().rss*1e-6)



    _times.append(("run", perf_counter()-_time))
    # process = psutil.Process(os.getpid())
    # print(process.memory_info().rss*1e-6)
    # #quit()

    # Saving complete stats as pandas
    data_frame = pd.DataFrame(stats, columns=stats.dtype.names, index=brain_names)
    F = BytesIO()
    data_frame.to_excel(F, merge_cells=False)
    writer.zip.writestr("complete_stats.xlsx", F.getbuffer())

    # Saving complete as npy
    F = BytesIO()
    np.savez(F, stats=stats, names=brain_names)
    writer.zip.writestr("complete_stats.npz", F.getbuffer())

    # Sorting stats so we only save the x amount of good snakes.
    stats[Stats.MOVES_PER_FOOD] *= -1
    indexes = np.argsort(stats, order=[Stats.LENGTH, Stats.MOVES_MADE, Stats.MOVES_PER_FOOD])[::-1]

    #indexes = np.argsort(stats, order=[Stats.LENGTH, Stats.MOVES_PER_FOOD, Stats.MOVES_MADE])[::-1]

    # Writing brains to zip
    brain_filenames = []
    for idx in range(min(max_save, indexes.shape[0])):
        brain_filenames.append(writer.write_brain(brains[indexes[idx]]))

    # Updating stats length
    stats = stats[indexes[:len(brain_filenames)]]

    # Saving stats as pandas
    data_frame = pd.DataFrame(stats, columns=stats.dtype.names, index=brain_filenames)
    F = BytesIO()
    data_frame.to_excel(F, merge_cells=False)
    writer.zip.writestr("cut_stats.xlsx", F.getbuffer())

    # Saving stats as npy
    F = BytesIO()
    np.savez(F, stats=stats, names=brain_filenames)
    writer.zip.writestr("cut_stats.npz", F.getbuffer())

    if close_file:
        writer.close()

    _times.append(("cleanup", perf_counter() - _time))

    pprint(_times)

    return writer.filename
