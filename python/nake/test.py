from brain import Brains, BasicBrain, CrossoverBrainGenerator, BasicBrainGenerator
from snake import Snake, SnakeActions
from board import Board
from food import FoodGenerator
from run import run_generator, Stats, run_snake
from snakeio import Reader

import consts
import matplotlib.pyplot as plt
import numpy as np


def callback_move(snake, board):
    im = snake.generatePreviewImage(board)
    plt.imshow(im, vmax=255)
    plt.show()


if __name__ == "__main__":

    foodGenerator = FoodGenerator(Board.fromDims(10, 10), (1, 1), 2321)
    snake = Snake.initializeAtPosition(
        (5,5),
        direction=consts.Moves.DOWN,
        name="loop",
        history=True,
        length=4
    )


    brain_generator = BasicBrainGenerator(n_generate=1000)

    i = 0
    while True:
        i+=1
        filepath = r"C:\tmp\generation.%04d.zip" % i

        term = run_generator(brain_generator, snake, foodGenerator, filepath)


        reader = Reader(filepath)
        ndata = reader.read_numpy("run_stats.npz")
        stats = ndata["stats"]
        file_paths = ndata["names"]

        sort_order =[
            Stats.LENGTH,
            Stats.MOVES_PER_FOOD,
            Stats.MOVES_MADE
        ]

        stats[Stats.MOVES_PER_FOOD]*=-1
        indexes = np.argsort(stats, order=[Stats.LENGTH, Stats.MOVES_PER_FOOD, Stats.MOVES_MADE])
        stats_sorted = stats[indexes]

        # print (file_paths[indexes[-1]])
        # print (stats_sorted[-2])

        # TODO use paths rather than indexes
        F = reader.read_bytesIO(reader.brains_info[indexes[-1]])
        b1 = Brains.load(F)

        # TODO use paths rather than indexes
        F = reader.read_bytesIO(reader.brains_info[indexes[-2]])
        b2 = Brains.load(F)

        _snake = snake.duplicate()
        _foodGenerator = foodGenerator.duplicate(initialState=True)
        term = run_snake(_snake, b1.duplicate(), _foodGenerator)

        print ("Term {} movesR {} perFood {} length {} movesM {}".format(
            term,
            _snake.movesRemaining,
            _snake.movesPerFood(),

            _snake.length,
            _snake.history.moves_made()
        ))
        print(stats_sorted[-2])
        print(stats_sorted[-1])

        brain_generator = CrossoverBrainGenerator(
            [b1, b2],
            n_generate=brain_generator.n_generate,
        )