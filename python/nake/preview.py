import subprocess
import os
import numpy as np

from brain import Brains, BasicBrain, CrossoverBrainGenerator, BasicBrainGenerator
from snake import Snake, SnakeActions
from board import Board
from food import FoodGenerator
from run import run_generator, Stats, run_snake
from snakeio import Reader
import consts

foodGenerator = FoodGenerator(Board.fromDims(10, 10), (1, 1), 2321)
snake = Snake.initializeAtPosition(
    (5, 5),
    direction=consts.Moves.DOWN,
    name="loop",
    history=True,
    length=4
)
#reader = Reader(r"C:\tmp\good\25_generation.0270.zip")
reader = Reader(r"C:\tmp\generation.0036.zip")
ndata = reader.read_numpy("run_stats.npz")
stats = ndata["stats"]
indexes = np.argsort(stats, order=[Stats.LENGTH, Stats.MOVES_PER_FOOD, Stats.MOVES_MADE])

F = reader.read_bytesIO(reader.brains_info[indexes[-1]])
b2 = Brains.load(F)



def close(proc):

    proc.stdin.close()
    if proc.stderr is not None:
        proc.stderr.close()
    proc.wait()



FFMPEG_BIN = 'ffmpeg'

command = [ FFMPEG_BIN,
        '-y', # (optional) overwrite output file if it exists
        '-f', 'rawvideo',
        '-s', '10x10', # size of one frame
        #'-pix_fmt', 'rgb24',
        '-pix_fmt', 'gray',
        '-r', '12', # frames per second
        '-i', '-', # The imput comes from a pipe
        '-an', # Tells FFMPEG not to expect any audio
        '-vcodec', 'libx264',
        #'-vcodec', 'raw',
        r'C:\tmp\28_generation.0036.mp4' ]

proc  = subprocess.Popen( command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)


im = np.ones([360,420], dtype=np.uint8)


def callback_move(snake, board, food):
    im = snake.generatePreviewImage(board)
    im[food[1], food[0]] = 255


    print (proc.stdin.write( im.tostring() ))


term = run_snake(snake, b2.duplicate(), foodGenerator, callback_move=callback_move)















