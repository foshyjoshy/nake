from brain import Brains, BasicBrain, CrossoverBrainGenerator, BasicBrainGenerator
from snake import Snake, SnakeActions
from board import Board
from food import FoodGenerator
from run import run_generator, run_snake, RunScenario
from run_stats import RunStats
from snakeio import Reader

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
        length=4
    )

    food_generator_01 = FoodGenerator(Board.fromDims(10, 10), (1, 1), 434343)
    scenario_01 = RunScenario(snake_01, food_generator_01)

    food_generator_02 = FoodGenerator(Board.fromDims(10, 10), (8, 1), 554545)
    scenario_02 = RunScenario(snake_01, food_generator_02)

    food_generator_03 = FoodGenerator(Board.fromDims(10, 10), (1, 8), 942)
    scenario_03 = RunScenario(snake_01, food_generator_03)

    food_generator_04 = FoodGenerator(Board.fromDims(10, 10), (8, 8), 876534)
    scenario_04 = RunScenario(snake_01, food_generator_04)


    scenarios = [
        scenario_01,
        scenario_02,
        scenario_03,
        scenario_04
    ]

    generator = BasicBrainGenerator(n_generate=100000)


    print (run_generator(generator, scenarios))