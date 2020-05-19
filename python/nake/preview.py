from logging import debug
import subprocess
import os
import numpy as np

FFMPEG_BIN = 'ffmpeg'

class VideoWriter:
    """ Simple ffmpeg video writer """

    DEFAULT_FPS = 12

    def __init__(self, file_path, input_width, input_height, override=True, fps=None, n_channels=0):
        if not override:
            if os.path.exists(file_path):
                raise Exception("File exists {}".format(file_path))
        dir_name = os.path.dirname(file_path)
        if not os.path.exists(dir_name):
            raise Exception("Dir doesn't exist {}".format(file_path))

        if n_channels == 0:
            pix_fmt = "gray"
        elif n_channels == 3:
            pix_fmt = "rgb24"
        else:
            raise Exception("n_channels {} not supported".format(n_channels))

        self.file_path = file_path
        self.input_width = input_width
        self.input_height = input_height

        self.command = [FFMPEG_BIN,
            '-y',

            '-f', 'rawvideo',
            '-s', '{}x{}'.format(input_width, input_height),
            '-pix_fmt', pix_fmt,
            '-r', '{:f}'.format(fps or self.DEFAULT_FPS),
            '-i', '-',
            '-an',
            '-vcodec', 'h264',
            self.file_path,
        ]

        self.proc = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE
        )


    def write_im(self, im):
        """ write image """
        try:
            return self.proc.stdin.write(im.tobytes())
        except IOError as err:
            _, ffmpeg_error = self.proc.communicate()
            ffmpeg_error = ffmpeg_error.decode()
            raise Exception(ffmpeg_error)

    def close(self):
        """ Closing subprocess"""
        if self.proc:
            self.proc.stdin.close()
            if self.proc.stderr is not None:
                self.proc.stderr.close()
            self.proc.wait()
            self.proc = None
            print ("closing")




def callback_move(vid_writer, snake, brain, board, food):

    im = snake.generatePreviewImage(board)
    im[food[1], food[0]] = 255

    im2 = np.zeros([16,16], dtype=np.uint8)
    im2[3:13, 3:13] = im

    print (vid_writer.write_im(im2))


    # print (brain.sequential_model.input_arr)
    # quit()









from brain import Brains, BasicBrain, CrossoverBrainGenerator, BasicBrainGenerator
from snake import Snake, SnakeActions
from board import Board
from food import FoodGenerator
from run import run_generator, Stats, run_snake
from snakeio import Reader
import consts


foodGenerator = FoodGenerator(Board.fromDims(10,10), (0,0), 2321)
snake = Snake.initializeAtPosition(
    (5, 5),
    direction=consts.Moves.DOWN,
    name="loop",
    history=True,
    length=4
)
reader = Reader(r"C:\tmp\generation.9780.zip")
#reader = Reader(r"C:\tmp\generation.0243.zip")
ndata = reader.read_numpy("cut_stats.npz")
stats = ndata["stats"]

F = reader.read_bytesIO(reader.brains_info[0])
brain1 = Brains.load(F)


import matplotlib.pyplot as  plt

plt.subplot(1,3,1)
plt.imshow(brain1.sequential_model[0].weights, vmin=-1, vmax=1, cmap="gray")

brain2 = brain1#.duplicate()
brain2.mutate(100)
plt.subplot(1,3,2)
plt.imshow(brain2.sequential_model[0].weights, vmin=-1, vmax=1, cmap="gray")
plt.subplot(1,3,3)

plt.imshow(brain2.sequential_model[0].weights-brain1.sequential_model[0].weights, vmin=-1, vmax=1, cmap="gray")
print (brain2.sequential_model[0].weights-brain1.sequential_model[0].weights)

plt.show()

quit()








vid_writer = VideoWriter(r"C:\tmp\aaa3.mp4", 16, 16)





from functools import partial#


term = run_snake(snake, b2.duplicate(), foodGenerator, callback_move=partial(callback_move, vid_writer))
print (vid_writer.file_path)














