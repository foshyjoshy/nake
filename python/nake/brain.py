import logging
import numpy as np
from neuralNet import Layer

import time

n_inputs = 24
n_outputs = 16

inputs = np.random.randint(0, 20, [n_inputs, 1])

layer1 = Layer("hidden_1", n_inputs, n_outputs)
layer2 = Layer("hidden_2", n_outputs, n_outputs)
layer3 = Layer("ouput", n_outputs, 4)

"""
for i in range(100):
    inputs = np.random.randint(0, 20, [n_inputs, 1])

    #a = time.time()
    ouput1 = layer1.compute(inputs)
    ouput2 = layer2.compute(ouput1)
    ouput3 = layer3.compute(ouput2)
    #print (time.time()-a)




    mo = ["left", "right", "up", "down"][np.argmax(ouput3)]
    print("move {} {}".format(mo, ""))
"""

class ssd:

    pass

s = time.time()
a = []


maxlength = 64*64

positions = np.zeros([10, 2], dtype=np.uint16)
headidx = 10
length = 4
direction = "Up"

d = positions[::-1]










