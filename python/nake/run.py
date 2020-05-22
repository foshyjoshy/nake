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
            print("ssss")
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
        RunStats.MOVES_PER_FOOD: snake.history.movesPerFood(),
        RunStats.LENGTH: snake.length,
        RunStats.DIRECTION: snake.direction.value,
    }




from preview import VideoWriter

class FlexiDraw:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.arrs = []

    def create_array(self):
        """ """
        return np.zeros((self.width, self.height), dtype=np.int64)

    def draw_snake(self, snake):
        """ """
        if snake.moves_made > len(self.arrs):
            self.arrs.append(self.create_array())
        idx = snake.moves_made-1
        pos = np.clip(snake.arr, (0,0), (self.height-1, self.width-1))
        #self.arrs[idx][pos[:,1], pos[:,0]]+=1

        head =  np.clip(snake.headPosition,(0,0), (self.height-1, self.width-1))

        self.arrs[idx][pos[:, 1], pos[:, 0]] += 1
        #self.arrs[idx][head[1], head[0]] += 1


    def draw_callback(self, snake, brain, board, food):
        self.draw_snake(snake)


    def write(self, file_path):


        im2 = np.zeros([16, 16], dtype=np.uint8)
        writer = VideoWriter(file_path, 16, 16)
        for arr in self.arrs:

            arr = arr*(255/np.max(arr))



            im2[3:13, 3:13] = arr.astype(np.uint8)



            print(writer.write_im(im2))










class RunScenario:
    """ used to create a scenario for running brains"""

    def __init__(self, snake, food_generator, duplicate_inputs=True):
        # Checking if inputs are correct
        isinstance(snake, Snake)
        isinstance(food_generator, FoodGenerator)

        # Checks if food its inside the current snake
        if snake.pointInside(food_generator):
            raise Exception("{} is inside snake".format(food_generator))

        if duplicate_inputs:
            self.snake = snake.duplicate()
            self.food_generator = food_generator.duplicate(
                initialState=True,
                keepBoard=False,  # makes sure we duplicate the board
            )
        else:
            self.snake = snake
            self.food_generator = food_generator

    @property
    def board(self):
        return self.food_generator.board

    def get_duplicated_snake(self):
        """ Returns a duplicate of the input snake """
        snake = self.snake.duplicate(duplicate_history=False)
        snake.set_empty_history()
        return snake

    def get_duplicated_food_generator(self):
        """ Return a duplicate of the input food generator"""
        return self.food_generator.duplicate(
            initialState=True,
            keepBoard=False,
        )

    def run_brain(self, brain, *args, **kwargs):
        """ Runs a brain through this scenario"""

        snake = self.get_duplicated_snake()
        food_generator = self.get_duplicated_food_generator()

        return run_snake(
            snake,
            brain,
            food_generator,
            board=food_generator.board,
            *args,
            **kwargs
        )


def run_generator(brain_generator, scenarios):
    """ Run a brain generator """

    #scenarios = [scenarios[0]]


    # Storing stats for every brain processed
    full_stats_stashs = [RunStatsStash(len(brain_generator)) for i in range(len(scenarios))]


    draw = FlexiDraw(10,10)

    scores = []

    for brain in brain_generator:

        total_score = 0
        for sidx, scenario in enumerate(scenarios):
            run_stats = scenario.run_brain(brain, callback_move=draw.draw_callback)
            full_stats_stashs[sidx].append(brain.name, **run_stats)

            max_length = scenario.board.size
            max_num_moves = (scenario.board.size - scenario.snake.length) \
                            * scenario.snake.moves_increase_by \
                            + scenario.snake.length

            max_moves_per_food = max_num_moves / scenario.board.size

            max_value = 1000000
            multiplier_length = max_value / float(max_length)
            multiplier_moves_per_food = multiplier_length / float(max_moves_per_food+1)
            multiplier_moves_made = multiplier_moves_per_food / float(max_num_moves+1)

            # Moves per food can been None is no food has been hit
            moves_per_food = run_stats[RunStats.MOVES_PER_FOOD] or max_moves_per_food
            r_moves_per_food = max_moves_per_food-float(moves_per_food)

            score = run_stats[RunStats.LENGTH] * multiplier_length
            score += r_moves_per_food * multiplier_moves_per_food
            score += run_stats[RunStats.MOVES_MADE] * multiplier_moves_made

            total_score += score

        scores.append(total_score / len(scenarios))


    # for idx in np.argsort(scores)[-10:]:
    #     for i in full_stats_stashs:
    #         print (i._stats[idx],)
    #     print ()


    import matplotlib.pyplot as plt



    draw.write(r"C:\tmp\render.mp4")

    quit()

    # for arr in draw.arrs:
    #     plt.imshow(arr)
    #     plt.show()
    #
    #
    #
    #
    # plt.plot(scores)
    # plt.show()
    #



    return full_stats_stashs
