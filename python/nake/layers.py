import numpy as np
from registry import Registry, RegistryItemBase
from activations import Activation, Tanh

class Layer(Registry):
    """ A class to store all layers"""
    registry = {}


class LayerBase(RegistryItemBase):
    """" Abstract base class for all layers to subclass """
    REGISTRY = Layer

    N_INPUTS = "n_inputs"
    N_OUTPUTS = "n_outputs"
    LAYER_NAME = "layer_name"
    ACTIVATION = "activation"
    USE_BIAS = "use_bias"



class Dense(LayerBase):
    """ Dsense layer """


    def __init__(self, layer_name, n_inputs, n_outputs, activation=None, use_bias=True):
        self.layer_name = layer_name
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.use_bias = use_bias

        if activation is None:
            activation = Activation.getInitialized("tanh")
        else:
            if not Activation.isObjectRegistered(activation):
                raise Exception("{} is not a "\
                "registered activation. Use {}".format(activation, Activation.registeredClasses()))

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

    def __getstate__(self):
        """ Returns the state of the layer"""
        state = {
            self.N_INPUTS :  self.n_inputs,
            self.N_OUTPUTS  : self.n_outputs,
            self.LAYER_NAME : self.layer_name,
            self.ACTIVATION : self.activation.__getstate__(),
            self.USE_BIAS : self.use_bias,
         }
        return {**super().__getstate__(), **state}




if __name__ == "__main__":

    import pprint

    act = Activation.getInitialized("relu")

    layer = Layer("dense", "input_layer", 10, 20, activation=act)
    state = layer.__getstate__()
    pprint.pprint(state)