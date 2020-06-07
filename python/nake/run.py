from snake import Snake
from brain import BrainBase
from food import FoodGenerator
from board import Board
from consts import Moves, Terminated
from run_stats import RunStats, RunStatsStash
import numpy as np
from callbacks import CallbackBase



def run_snake(snake, brain, foodGenerator, board=None, callbacks=None):
    """ Runs snake until it terminates"""
    callbacks = callbacks or []
    if board is None:
        board = foodGenerator.board

    # Checking inputs
    assert isinstance(snake, Snake)
    assert isinstance(foodGenerator, FoodGenerator)
    assert isinstance(board, Board)
    assert isinstance(brain, BrainBase)
    for callback in callbacks:
        assert isinstance(callback, CallbackBase)


    while snake.canMove():
        previous_move = snake.direction

        # Using brain to compute move
        move = Moves(brain.computeMove(snake, board, foodGenerator))
        # Moving snake
        snake.move(move)

        # Run any snake moved callbacks
        for callback in callbacks:
            callback.snake_moved(snake, brain, board, foodGenerator.pos)

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

    # Run any terminated callbacks
    for callback in callbacks:
        callback.snake_terminated(term, snake, brain, board, foodGenerator.pos)

    return {
        RunStats.TERM: term,
        RunStats.MOVES_REMAINING: snake.movesRemaining,
        RunStats.MOVES_MADE: snake.history.moves_made(),
        RunStats.MOVES_PER_FOOD: snake.history.movesPerFood(),
        RunStats.LENGTH: snake.length,
        RunStats.DIRECTION: snake.direction.value,
    }




class RunScenario:
    """ used to create a scenario for running brains"""

    def __init__(self, snake, food_generator, duplicate_inputs=True, callbacks=None):
        # Checking if inputs are correct
        isinstance(snake, Snake)
        isinstance(food_generator, FoodGenerator)
        self.callbacks = callbacks

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

    def run_brain(self, brain, *args, callbacks=None, **kwargs):
        """ Runs a brain through this scenario"""

        snake = self.get_duplicated_snake()
        food_generator = self.get_duplicated_food_generator()

        return run_snake(
            snake,
            brain,
            food_generator,
            board=food_generator.board,
            *args,
            callbacks=(callbacks or []) + (self.callbacks or []),
            **kwargs
        )




def run_generator(brain_generator, scenarios, scorer, callbacks=None):
    """ Run a brain generator """

    # Storing stats for every brain processed
    full_stats_stash = [RunStatsStash(len(brain_generator)) for i in range(len(scenarios))]

    # Full scores
    full_scores = np.zeros([len(brain_generator), len(scenarios)])

    brains = []
    for b_idx, brain in enumerate(brain_generator):
        for s_idx, scenario in enumerate(scenarios):
            # Running brain
            run_stats = scenario.run_brain(brain, callbacks=callbacks)
            # Stashing run stats
            full_stats_stash[s_idx].append(brain.name, **run_stats)
            # Scoring stats
            full_scores[b_idx, s_idx] = scorer.score_stats(**run_stats)

        mean_score = np.mean(full_scores[b_idx])
        brains.append((mean_score, brain))
        brains.sort(key=lambda x: -x[0])
        brains = brains[:25]

    return full_stats_stash, full_scores, [i[1] for i in brains]

