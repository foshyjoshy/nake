import numpy as np


class Layer():

    def __init__(self, name, n_inputs, n_outputs, activation=None, use_bias=True):
        self.name = name
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.use_bias = use_bias
        self.activation = activation or np.tanh

        # Between -1 and 1 #TODO REMOVE / n_inputs
        self.weights = (np.random.random([n_outputs, n_inputs]) * 2 - 1)# / n_inputs

        # Between -1 and 1
        self.biases = (np.random.random([n_outputs, 1]) * 2 - 1) * 0.001
        if not use_bias:
            self.biases[:] = 0

    def setWeights(self, weights):
        """ Setting weights on layer (n_outputs x n_inputs) """
        if not weights.shape ==  self.weights.shape:
            raise ValueError("shape mismatch: {} - {}".format(weights.shape, self.weights.shape))
        self.weights[:] = weights.copy()

    def setBiases(self, biases):
        """ Setting biases on layer (n_outputs x 1)"""
        if not biases.shape ==  self.biases.shape:
            raise ValueError("shape mismatch: {} - {}".format(biases.shape, self.biases.shape))
        self.biases = biases.copy()

    def compute(self, inputs):
        """ Runs the layer """
        values = np.matmul(self.weights, inputs) + self.biases
        outputs = self.activation(values)
        return outputs