from brain import Brains, BasicBrain2, CrossoverBrainGenerator, BasicBrainGenerator
from snake import Snake, SnakeActions
from board import Board
from food import FoodGenerator
from run import run_generator, run_snake, RunScenario
from scoring import ScoreRun
from snakeio import Writer, Reader
from callbacks import FlexiDraw
from run_stats import RunStats
import consts
import matplotlib.pyplot as plt
import numpy as np
import time
from run_stats import RunStats, RunStatsStash


#TODO save out brain generators... add import brains into generated set. As fist or last brains
#TODO create config for brain generators, mutation and crossover.

#TODO SAVE RENDER WITH BRAINS?
#TODO fix run generation



if __name__ == "__main__":

    movesRemaining = 60
    moves_increase_by = 90
    snake_01 = Snake.initializeAtPosition(
        (15,15),
        direction=consts.Moves.DOWN,
        name="loop",
        history=True,
        length=4,
        movesRemaining=movesRemaining,
        moves_increase_by=movesRemaining,
    )

    snake_02 = Snake.initializeAtPosition(
        (15,15),
        direction=consts.Moves.UP,
        name="loop",
        history=True,
        length=4,
        movesRemaining=movesRemaining,
        moves_increase_by=movesRemaining,
    )
    snake_03 = Snake.initializeAtPosition(
        (15,15),
        direction=consts.Moves.LEFT,
        name="loop",
        history=True,
        length=4,
        movesRemaining=movesRemaining,
        moves_increase_by=movesRemaining,
    )
    snake_04 = Snake.initializeAtPosition(
        (15,15),
        direction=consts.Moves.RIGHT,
        name="loop",
        history=True,
        length=4,
        movesRemaining=movesRemaining,
        moves_increase_by=movesRemaining,
    )

    board = Board.fromDims(31, 31)

    #food_generator_01 = FoodGenerator(board, (1, 1), 434343)
    # scenario_01 = RunScenario(snake_01, food_generator_01)
    #
    # food_generator_02 = FoodGenerator(board, (9, 1), 5545245)
    # scenario_02 = RunScenario(snake_01, food_generator_02)
    #
    # food_generator_03 = FoodGenerator(board, (1, 9), 9242)
    # scenario_03 = RunScenario(snake_02, food_generator_03)
    #
    # food_generator_04 = FoodGenerator(board, (9, 9), 8534)
    # scenario_04 = RunScenario(snake_02, food_generator_04)

    # scenarios = [
    #     scenario_01,
    #     scenario_02,
    #     scenario_03,
    #     scenario_04
    # ]


    start_positions = [
        (1,1),
        (1,29),
        (29,1),
        (29,29),
        (10,10),
        (10,20),
        (20,10),
        (20,20),
        (1,15),
        (15,1),
        (15,29),
        (29,15)
    ]

    randomState = np.random.RandomState(seed=34235)

    scenarios = []
    for start_position in start_positions:
        for snake in [snake_01, snake_02, snake_03, snake_04]:
            seed = randomState.randint(0, 2 ** 32 - 1, dtype=np.uint32)
            food_generator = FoodGenerator(board, start_position, seed)
            scenario = RunScenario(snake, food_generator)
            scenarios.append(scenario)

    full_scenarios = scenarios

    #"""
    # Creating a basic brain generator
    brain = BasicBrain2.create(
        activation="leakyrelu",
        name="generator_input",
        n_hidden_inputs=18,
        n_hidden_layers=2,
    )
    generator = BasicBrainGenerator(brain=brain, n_generate=100)
    #"""

    # reader = Reader(r"C:\tmp\New folder\generation.0158.zip")
    # brain = Brains.load(reader.read_numpy(reader.brains_info[0]))
    #
    # reader = Reader(r"C:\tmp\New folder\generation.0182.zip")
    # brain2 = Brains.load(reader.read_numpy(reader.brains_info[0]))
    #
    #
    # reader = Reader(r"C:\tmp\New folder\generation.0310.zip")
    # brain3 = Brains.load(reader.read_numpy(reader.brains_info[0]))
    #
    # generator = CrossoverBrainGenerator(
    #     brains=[brain, brain2, brain3],
    #     n_generate=100,
    # )


    # Using this to score the run
    scorer = ScoreRun.from_scenario(scenarios[0])

    scenario_score_weights = None

    # Choosing initial scenarios
    indexes = np.random.choice(len(full_scenarios), 10)
    scenarios = full_scenarios#[full_scenarios[i] for i in indexes]
    print ("Picked scenarios", indexes)


    generation = 0
    while True:
        generation += 1
        print ("Running generation {}".format(generation))

        np.random.choice(5, 3)

        draw_callback = FlexiDraw(board.width, board.height)

        # indexes = np.random.choice(len(full_scenarios), 8)
        # scenarios = [full_scenarios[i] for i in indexes]
        # print ("Picked scenarios", indexes)

        # for scenario in scenarios:
        #     scenario.callbacks = [FlexiDraw(board.width, board.height)]

        im = np.zeros((board.height,board.width), dtype=np.uint8)
        for scenario in scenarios:
            im[scenario.food_generator.pos[1], scenario.food_generator.pos[0]] = 255
        draw_callback.prepend_arrs.append(im)

        for scenario in scenarios:
            # im = np.zeros((11, 11), dtype=np.uint8)
            # im[scenario.food_generator.pos[1], scenario.food_generator.pos[0]] = 255
            # draw_callback.prepend_arrs.append(im)

            im = scenario.snake.generatePreviewImage(scenario.board, color_head=155, color_body=100)
            im[scenario.food_generator.pos[1], scenario.food_generator.pos[0]] = 255
            draw_callback.prepend_arrs.append(im)




        full_stats_stash, full_scores, brains = run_generator(
            generator,
            scenarios,
            scorer,
            callbacks = [draw_callback],
            scenario_score_weights=scenario_score_weights,
        )

        path = r"C:\tmp\generation.{:04d}.zip".format(generation)
        writer = Writer(path)
        for brain in brains:
            writer.write_brain(brain)

        writer.write_snake(snake_01, "snake_01")
        writer.write_snake(snake_02, "snake_02")
        writer.write_snake(snake_03, "snake_03")
        writer.write_snake(snake_04, "snake_04")
        for idx, stats_stash in enumerate(full_stats_stash):
            writer.write_stats(stats_stash, "full_stats_{:02d}".format(idx))

        writer.write_numpy_arr(indexes, "picked_scenario_indexes")
        writer.write_numpy_arr(full_scores, "full_scores")

        writer.close()

        # Creating generator
        generator = CrossoverBrainGenerator(
            brains=brains[:2],
            n_generate=generator.n_generate,
        )


        for idx in range(1)[::-1]:
            print (idx)
            default_count = 0
            for s_idx, stats in enumerate(full_stats_stash):
                print (stats.get_stats_for_brain(brains[idx]))
                if stats.get_stats_for_brain(brains[idx])[RunStats.LENGTH] == 4:
                    default_count+=1
            print ("Default count {}/{}".format(default_count, len(full_stats_stash)))

        #Runn best brain over all scenarios

        # scores = np.zeros(len(full_scenarios))
        # for sidx, scenario in enumerate(full_scenarios):
        #     for brain in generator.brains:
        #         run_stats = scenario.run_brain(brain)
        #         scores[sidx] += scorer.score_stats(**run_stats)
        #

        # print (np.sort(scores))
        # print ("scenario indexes {}".format(np.argsort(scores)[:10]))
        # scenarios = [full_scenarios[i] for i in np.argsort(scores)[:10]]

        # indexes = np.random.choice(len(full_scenarios), 10)
        # print ("Used indexes", indexes)
        # scenarios = [full_scenarios[i] for i in indexes]

        scenarios = full_scenarios
        for scenario in scenarios:
            new_food = FoodGenerator(
                scenario.board,
                scenario.food_generator._initialPos.copy()
            )
            scenario.food_generator = new_food



        #quit()



        # scenario_snake_length = np.ones(len(scenarios))
        # for s_idx, stats in enumerate(full_stats_stash):
        #     scenario_stats = stats.get_stats_for_brain(brains[0])
        #     scenario_snake_length[s_idx] = scenario_stats[RunStats.LENGTH]
        #
        #
        # scenario_snake_length -= np.min(scenario_snake_length)
        # if sum(scenario_snake_length) > 0:
        #     scenario_snake_length *= (1.0/np.max(scenario_snake_length))
        #     scenario_score_weights = 1-(scenario_snake_length)
        #
        #     scenario_score_weights = scenario_score_weights*0.7+0.3
        #
        # else:
        #     scenario_score_weights = np.ones_like(scenario_snake_length)





        path = r"C:\tmp\generation.{:04d}.avi".format(generation)
        draw_callback.write(path)
        # for sidx, scenario in enumerate(scenarios):
        #     scenario.callbacks[0].write(r"C:\tmp\generation.{:04d}.{:02d}.mp4".format(generation, sidx))
        print (path)
        #quit()


