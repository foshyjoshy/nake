from brain import Brains, BasicBrain2, CrossoverBrainGenerator, BasicBrainGenerator
from snake import Snake, SnakeActions
from board import Board
from food import FoodGenerator
from run import run_generator, run_snake, RunScenario
from scoring import ScoreRun
from snakeio import Writer
from callbacks import FlexiDraw

import consts
import matplotlib.pyplot as plt
import numpy as np
import time


#TODO save out brain generators... add import brains into generated set. As fist or last brains
#TODO create config for brain generators, mutation and crossover.

#TODO SAVE RENDER WITH BRAINS?
#TODO fix run generation



if __name__ == "__main__":

    snake_01 = Snake.initializeAtPosition(
        (5,5),
        direction=consts.Moves.DOWN,
        name="loop",
        history=True,
        length=4,
        movesRemaining=40
    )

    snake_02 = Snake.initializeAtPosition(
        (5,5),
        direction=consts.Moves.UP,
        name="loop",
        history=True,
        length=4,
        movesRemaining=40
    )




    board = Board.fromDims(11, 11)

    food_generator_01 = FoodGenerator(board, (1, 1), 434343)
    scenario_01 = RunScenario(snake_01, food_generator_01)

    food_generator_02 = FoodGenerator(board, (9, 1), 5545245)
    scenario_02 = RunScenario(snake_01, food_generator_02)

    food_generator_03 = FoodGenerator(board, (1, 9), 9242)
    scenario_03 = RunScenario(snake_02, food_generator_03)

    food_generator_04 = FoodGenerator(board, (9, 9), 8534)
    scenario_04 = RunScenario(snake_02, food_generator_04)
    #
    # im = snake_01.generatePreviewImage(food_generator_01.board)
    #
    # im[food_generator_01.pos[1], food_generator_01.pos[0]] = 255
    # im[food_generator_02.pos[1], food_generator_02.pos[0]] = 255
    # im[food_generator_03.pos[1], food_generator_03.pos[0]] = 255
    # im[food_generator_04.pos[1], food_generator_04.pos[0]] = 255

    # plt.imshow(im)
    # plt.show()



    scenarios = [
        scenario_01,
        scenario_02,
        scenario_03,
        scenario_04
    ]


    # Creating a basic brain generator
    brain = BasicBrain2.create(activation="leakyrelu", name="generator_input")
    generator = BasicBrainGenerator(brain=brain, n_generate=100000)


    # Using this to score the run
    scorer = ScoreRun.from_scenario(scenario_01)

    generation = 0
    while True:
        generation += 1
        print ("Running generation {}".format(generation))

        draw_callback = FlexiDraw(11,11)
        for scenario in scenarios:
            scenario.callbacks = [FlexiDraw(11,11)]

        full_stats_stash, full_scores, brains = run_generator(
            generator,
            scenarios,
            scorer,
            callbacks = [draw_callback],
        )

        path = r"C:\tmp\generation.{:04d}.zip".format(generation)
        writer = Writer(path)
        for brain in brains:
            writer.write_brain(brain)
        writer.close()

        # Creating generator
        generator = CrossoverBrainGenerator(
            brains=brains[:4],
            n_generate=100000,
        )

        for idx in range(2)[::-1]:
            print ()
            for s_idx, stats in enumerate(full_stats_stash):
                print (stats.get_stats_for_brain(brains[idx]))


        path = r"C:\tmp\generation.{:04d}.mp4".format(generation)
        draw_callback.write(path)
        for sidx, scenario in enumerate(scenarios):
            scenario.callbacks[0].write(r"C:\tmp\generation.{:04d}.{:02d}.mp4".format(generation, sidx))
        print (path)


