import numpy as np
from registry import Registry, RegistryItemBase
from activations import Activation


class Layer(Registry):
    """ A class to store all layers"""
    registry = {}


class LayerBase(RegistryItemBase):
    """" Abstract base class for all layers to subclass """
    REGISTRY = Layer


class Dense(LayerBase):
    """ Dsense layer """

    def __init__(self, layer_name, n_inputs, n_outputs, activation=None, use_bias=True):
        self.layer_name = layer_name
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.use_bias = use_bias

        if activation is None:
            activation = Activation.getInitialized("tanh")
        self.activation = activation

        # Between -1 and 1
        self.weights = (np.random.random([n_outputs, n_inputs]) * 2 - 1)

        # Between -1 and 1
        self.biases = (np.random.random([n_outputs, 1]) * 2 - 1) * 0.001


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
        values = np.matmul(self.weights, inputs) + [0, self.biases][self.use_bias]
        outputs = self.activation.compute(values)
        return outputs



if __name__ == "__main__":


    layer = Layer("dense", "input_layer", 10, 20)
    print (Layer.registeredNames())