import logging
import numpy as np
from layers import Dense
import time


class Brain():
    """ Basic snake brain"""



    def __init__(self, n_inputs=14, n_hidden_inputs=16, n_outputs=4):
        super().__init__()

        self.layers = [
                Dense("input_layer", n_inputs, n_hidden_inputs),
                Dense("hidden_00", n_hidden_inputs, n_hidden_inputs),
                Dense("hidden_01", n_hidden_inputs, n_hidden_inputs),
                Dense("output_layer", n_hidden_inputs, n_outputs),
                     ]

        self.input_arr = self.generateRandomInputs()

    @property
    def n_inputs(self):
        """ Returns """
        return self.layers[0].n_inputs

    @property
    def n_outputs(self):
        """ Returns """
        return self.layers[-1].n_outputs

    def generateRandomInputs(self, minval=0, maxval=20):
        """ Generate random inputs values for testing"""
        return np.random.randint(minval, maxval, [self.n_inputs, 1])

    def compute(self, inputs=None):
        """ Runs the input values through the network"""
        if inputs is None: inputs = self.input_arr
        for layer in self.layers:
            inputs = layer.compute(inputs)
        return np.argmax(inputs)

    def crossover(self, brain2):
        """ Mixes two brains together"""
        pass

    def mutate(self, percent=5):
        """ Mutates a percentage of the non-locked networks weights """
        pass


class Brain2(Brain):
    pass




if __name__ == "__main__":

    a = Brain()
    quit()


    brain = Brain()

    input = brain.generateRandomInputs()

    a = time.time()
    for i in range(10000):
        c = brain.compute(input)
    print (time.time()-a)
    print (c)

