import numpy as np
import matplotlib.pyplot as plt
from board import Board
import time

import random

board = Board.fromDims(128, 64)

im = np.zeros([board.height,board.width], dtype=np.bool)


positions = np.mgrid[0:board.width,0:board.height].T.reshape([-1, 2])
np.random.shuffle(positions)
positions = positions[:int(board.height*board.width*0.9)]

numvalues = board.width*board.height
print ("Num values", numvalues)
# #"""
# a = time.time()
# for i in range(1000):
#     im[:] = False
#     im[positions[:,1], positions[:,0]] = 1
#     y, x = np.where(im==1)
#     index = random.randint(0, y.shape[0]-1)
#     im[y[index], x[index]] = 1
# print (time.time()-a)
# #plt.imshow(im)
# #plt.show()
# #"""

arr = np.zeros([numvalues], dtype=np.bool)
positions = np.arange(numvalues)
np.random.shuffle(positions)
positions = positions[:int(numvalues*0.6)]
print ("Snake length", positions.shape[0])
a = time.time()
for i in range(1000):
    arr[:] = False
    arr[positions] = True
    indexes = np.where(arr == False)[0]
    index = random.randint(0, indexes.shape[0]-1)

    y = int(index/board.width)
    x = index-(y*board.width)

print (time.time()-a)


arr2 = np.arange(numvalues)

a = time.time()
for i in range(1000):
    arr[:] = True
    arr[positions] = False
    indexes = arr2[arr == False]
    index = random.randint(0, indexes.shape[0]-1)

    y = int(index/board.width)
    x = index-(y*board.width)

print (time.time()-a)

quit()


# #im = arr.reshape([board.height, board.width])
# #plt.imshow(im)
# #plt.show()


arr = np.arange(numvalues)
positions = np.arange(numvalues)
np.random.shuffle(positions)
positions = positions[:int(numvalues*0.1)]
a = time.time()
for i in range(1000):
    #mask = np.in1d(arr, positions, invert=False,assume_unique=True)
    np.intersect1d(arr, positions)

print (time.time()-a)

#im = arr.reshape([board.height, board.width])
#plt.imshow(im)
#plt.show()












