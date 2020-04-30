from brain import Brains, BasicBrain, CrossoverBrainGenerator, BasicBrainGenerator
from snake import Snake, SnakeActions
from board import Board
from food import FoodGenerator

import consts
import time
import matplotlib.pyplot as plt
import run


from snakeio import Reader

#TODO WRITE GENERATORS
#TODO WRITE PANDA  ...Save term

#TODO Get fitness from these above


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

    filepath = r"C:\tmp\run.zip"
    brain_generator = BasicBrainGenerator(n_generate=1000)
    term = run.run_generator(brain_generator, snake, foodGenerator, filepath)

    print ("Opening")
    reader = Reader(filepath)

    # for f in reader.zip.namelist():
    #     zinfo = reader.zip.getinfo(f)
    #     print (zinfo)
    #     if(zinfo.is_dir()):
    #         print(f)

    print (reader.nr_brains,reader.brains_info)
    print (reader.nr_foods,reader.foods_info)
    print (reader.nr_snakes,reader.snake_info)