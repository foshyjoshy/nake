import brain
import snakeio
from board import Board
from food import FoodGenerator
from run import run_generator, run_snake, RunScenario,RunStats
from preview import VideoWriter

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from callbacks import CallbackBase,TestCallback
import io

file_path = r"C:\tmp\generation_4.0177.zip"

reader = snakeio.Reader(file_path)

brains = []
for bidx in range(len(reader.brains_info)):
    brains.append(reader.read_brain_via_index(bidx))
print (brains[0].sequential_model)

arrrr = []
for bidx in range(len(reader.brains_info)):
    for fidx in range(reader.nr_foods):
        snake = reader.read_snake_via_index(0)
        snake.set_empty_history()
        food_generator = reader.read_food_via_index(fidx)
        board = food_generator.board
        results = run_snake(snake, brains[bidx], food_generator)

        arrrr.append((results[RunStats.LENGTH], bidx, fidx))

print (arrrr)
arrrr = np.array(arrrr)

index =  np.argmax(arrrr[:,0])
print (arrrr[index])
bidx = arrrr[index,1]
fidx = arrrr[index,2]

snake = reader.read_snake_via_index(0)
snake.set_empty_history()
food_generator = reader.read_food_via_index(fidx)
board = food_generator.board
brain = brains[bidx]
scenario = RunScenario(snake, food_generator)

#results = run_snake(snake, brains[bidx], food_generator)
#
# print (results[RunStats.LENGTH])
#
# quit()
#


#
#
# brain.computeMove(snake, board, food_generator)
# print (brain.sequential_model.input_arr)
#
# data = []
# row_labels = [
#     "moves top board ",
#     "moves right board",
#     "moves bottom board",
#     "moves left board",
#     "moves to food 000%",
#     "moves to food 045%",
#     "moves to food 090%",
#     "moves to food 135%",
#     "moves to food 180%",
#     "moves to food 225%",
#     "moves to food 270%",
#     "moves to food 315%",
#     "moves to self 000%",
#     "moves to self 045%",
#     "moves to self 090%",
#     "moves to self 135%",
#     "moves to self 180%",
#     "moves to self 225%",
#     "moves to self 270%",
#     "moves to self 315%",
# ]
#
# inputs = brain.sequential_model.input_arr.flatten().copy()
# # inputs[inputs == -1] = np.nan
# data = np.array([row_labels, inputs]).T
#
# fig, axs = plt.subplots(1, 2, dpi=100, figsize=(10, 5))
# axs[0].axis('off')
# # axs[1].axis('off')
# the_table = axs[0].table(
#     cellText=data,
#     # rowLabels=row_labels,
#     # colLabels=['',"inputs"],
#     loc='center',
#     rowLoc='right')
# axs[0].axis('tight')
#
# im = snake.generatePreviewImage(board)
# im[food_generator.y, food_generator.x] = 122
# axs[1].imshow(im)
#
# # Remove whitespace from around the image
# # fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
#
# axs[1].set_aspect(1)
# axs[1].set_yticks(np.arange(30) + 0.5, minor='True')
# axs[1].set_xticks(np.arange(30) + 0.5, minor='True')
# axs[1].yaxis.grid(True, which='minor')
# axs[1].xaxis.grid(True, which='minor')
#
#
# plt.show()
# quit()





#
class Check(CallbackBase):

    def __init__(self, filepath, board):
        self.writer = VideoWriter(
            filepath,
            1000,
            500,
            vcodec="libx264",
            n_channels=3,
        )


    def snake_move_computed(self, move, snake, brain, board, food_position):
        """ call back before snake moves """
        print ("move:")
        data = []
        row_labels =[
            "moves top board ",
            "moves right board",
            "moves bottom board",
            "moves left board",
            "moves to food 000%",
            "moves to food 045%",
            "moves to food 090%",
            "moves to food 135%",
            "moves to food 180%",
            "moves to food 225%",
            "moves to food 270%",
            "moves to food 315%",
            "moves to self 000%",
            "moves to self 045%",
            "moves to self 090%",
            "moves to self 135%",
            "moves to self 180%",
            "moves to self 225%",
            "moves to self 270%",
            "moves to self 315%",
        ]

        inputs =  brain.sequential_model.input_arr.flatten().copy()
        #inputs[inputs == -1] = np.nan
        data = np.array([row_labels[:len(inputs)], inputs]).T

        fig, axs =plt.subplots(1,2, dpi=100, figsize=(10,5))
        axs[0].axis('off')
        #axs[1].axis('off')
        the_table = axs[0].table(
            cellText=inputs[None, ...],
            #rowLabels=row_labels,
            #colLabels=['',"inputs"],
            loc='center',
            rowLoc='right')
        axs[0].axis('tight')



        im = snake.generatePreviewImage(board)
        im[food_position[1],food_position[0]] = 122
        axs[1].imshow(im)


        # Remove whitespace from around the image
        #fig.subplots_adjust(left=0,right=1,bottom=0,top=1)

        axs[1].set_aspect(1)
        axs[1].set_yticks(np.arange(30)+0.5, minor='True')
        axs[1].set_xticks(np.arange(30)+0.5, minor='True')
        axs[1].yaxis.grid(True, which='minor')
        axs[1].xaxis.grid(True, which='minor')

        #fig.show()

        # #self.writer
        # fig.canvas.draw()
        #
        # print (576*576)
        #
        # # Now we can save it to a numpy array.
        # a = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        # print (a.shape)

        io_buf = io.BytesIO()
        fig.savefig(io_buf, format='raw')
        io_buf.seek(0)
        img_arr = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
                             newshape=(1000,500, -1))
        io_buf.close()

        print (img_arr.shape)
        self.writer.write_im(img_arr[:,:,:3])

        # if self.writer.frame_count > 20:
        #     self.writer.close()
        #     quit()

        plt.close(fig)
        print (self.writer.frame_count)


callback = Check( r"C:\tmp\test_12.mp4", board)

stats =scenario.run_brain(brain, callbacks=[callback])
callback.writer.close()
print (stats)