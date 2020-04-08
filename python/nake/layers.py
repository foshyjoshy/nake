import numpy as np
from abc import abstractmethod
from registry import Registry, RegistryItemBase
from activations import Activation, Tanh
from logging import debug
import math



class SequentialModel():
    """ A list of layers that is computed sequential """

    def __init__(self, layers):
        for idx, layer in enumerate(layers):
            # Converting layer dict (getstate) to Layer objects
            if isinstance(layer, dict):
                layers[idx] = Layer(**layer)

        #TODO check if layers work!!!

        self.layers = layers
        self.input_arr = self.generateRandomInputs()

    def __str__(self):
        return "SequentialModel({}x{}x{})".format(
            self.n_inputs, self.n_outputs, self.n_layers)

    def __iter__(self):
        for elem in self.layers:
            yield elem

    def __getitem__ (self, index):
        return self.layers[index]

    def layerByName(self, name):
        """ returns the layer for the given name"""
        for layer in self:
            if name == layer.layer_name:
                return layer

    @property
    def n_inputs(self):
        """ Returns """
        return self.layers[0].n_inputs

    @property
    def n_outputs(self):
        """ Returns """
        return self.layers[-1].n_outputs

    @property
    def n_layers(self):
        """ Returns """
        return len(self.layers)

    def generateRandomInputs(self, minval=0, maxval=20):
        """ Generate random inputs values for testing"""
        return np.random.randint(minval, maxval, [self.n_inputs, 1])

    def compute(self, inputs=None):
        """ Runs the input values through the network"""
        if inputs is None: inputs = self.input_arr
        for layer in self.layers:
            inputs = layer.compute(inputs)
        return np.argmax(inputs)

    def getStateList(self):
        """ Return a list of layer get state"""
        return [layer.__getstate__() for layer in self]

    def getWeights(self):
        """ Returns the array state of all layers"""
        arrWeights= {}
        for layer in self:
            for key, value in layer.getWeights().items():
                arrWeights["{}_{}".format(layer.layer_name, key)] = value
        return arrWeights

    def setWeights(self, arrDict):
        """ Sets arrays on layers """
        for name, arr in arrDict.items():
            debug("Setting arr {} with shape {}".format(name , arr.shape))
            name, arr_name = name.rsplit("_", 1)
            self.layerByName(name).setArr(arr_name, arr)

    def isCrossCompatible(self, other):
        """ Checks if the other model is cross compatible """
        if isinstance(other, SequentialModel):
            if other.n_layers == self.n_layers:
                for idx, layer in enumerate(self.layers):
                    if not layer.isCrossCompatible(other.layers[idx]):
                        break
                else:
                    return True
        return False

    def mutate(self, percent=5):
        """ Mutates a percentage of the non-locked weights """
        # This is very basic mutation
        percentages = np.random.randint(percent+1, size=self.n_layers)
        for idx, layer in enumerate(self):
            layer.mutate(percent=percentages[idx])

    def crossover(self, *others):
        """ Crossing n number of layers """

        # Checking if others are cross compatible
        for other in others:
            if not self.isCrossCompatible(other):
                raise Exception("Unable to crossover {} with {}".format(other, self))

        results = []
        # Crossing over layers
        for idx, layer in enumerate(self):
            results.append(layer.crossover(*[other[idx] for other in others]))
        return results




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

    BIASES = "biases"
    WEIGHTS = "weights"

    @abstractmethod
    def mutate(self, percent=5):
        """ Mutates a percentage of the non-locked weights """
        pass

    @abstractmethod
    def isCrossCompatible(self, other):
        """ Checks if other layer is cross compatible"""

    @abstractmethod
    def crossover(self, *others):
        """ Crossing n number of layers """





class Dense(LayerBase):
    """ Dense layer """

    def __init__(self, layer_name, n_inputs, n_outputs, activation=None, use_bias=True):
        self.layer_name = layer_name
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.use_bias = use_bias

        if activation is None:
            activation = Activation.getInitialized("tanh")
        else:
            if not Activation.isObjectRegistered(activation):
                if not isinstance(activation, dict):
                    raise Exception("{} is not a "\
                    "registered activation. Use {}".format(activation, Activation.registeredClasses()))
                else:
                    activation = Activation(**activation)

        self.activation = activation

        # Between -1 and 1
        self.weights = (np.random.random([n_outputs, n_inputs]) * 2 - 1)
        # Between -1 and 1
        self.biases = (np.random.random([n_outputs, 1]) * 2 - 1) * 0.001

        # Mutation mask ... create only once.
        self.mutation_mask = np.zeros_like(self.weights)


    def __str__(self):
        return "{}({}x{},use_bias={})".format(
            self.__class__.__name__, self.n_inputs, self.n_outputs, self.use_bias)

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

    def getWeights(self):
        """ Returns the array state of the layer"""
        return {
            self.WEIGHTS : self.weights,
            self.BIASES : self.biases,
        }

    def setArr(self, name, arr):
        """ Sets an arr"""
        if name == self.BIASES:
            self.setBiases(arr)
        elif name == self.WEIGHTS:
            self.setWeights(arr)
        else:
            raise Exception("{} is not a valid array name".format(name))

    def mutate(self, percent=2, setvalues=True):
        """ Mutates a percentage of the non-locked weights """
        # Using ceil makes sure at least one weight is mutates
        mutate_number = math.ceil((float(self.weights.size)/100)*percent)

        # Getting mutate_number of weight indexes
        float_indexes = np.random.random_sample(mutate_number)
        indexes = np.unique((float_indexes*self.weights.size).astype(int))
        indexes = np.unravel_index(indexes, self.weights.shape)

        random_values = np.random.random_sample(indexes[0].shape[0])*2-1

        if setvalues:
            # Setting random weights between -1 and 0
            self.weights[indexes] = random_values
        else:
            self.weights[indexes] = np.clip(self.weights[indexes] + (random_values*0.1), -1, 1)

    def isCrossCompatible(self, other):
        """ Checks if other layer is cross compatible"""
        if isinstance(other, self.__class__):
            return self.weights.shape == other.weights.shape
        else:
            return False

    def crossover(self, *others):
        """ Crossing n number of layers """
        for other in others:
            if not self.isCrossCompatible(other):
                raise Exception("{} is not cross compatible with {}".format(self, other))

        # Crossover Weights
        weight_mask = np.random.randint(len(others)+1, size=self.weights.shape)
        for idx, other in enumerate(others, start=1):
            mask = weight_mask == idx
            self.weights[mask] = other.weights[mask]

        # Crossover Biases
        biases_mask = np.random.randint(len(others)+1, size=self.biases.shape)
        for idx, other in enumerate(others, start=1):
            mask = biases_mask == idx
            self.biases[mask] = other.biases[mask]

        # Crossover use_bias
        bias_index = np.random.random_integers(0, len(others))
        if bias_index > 0:
            self.use_bias = others[bias_index-1].use_bias

        return (weight_mask, biases_mask, bias_index)




if __name__ == "__main__":

    layer = Layer("dense", "input_layer", 10, 20)
    layer2 = Layer("dense", "output_layer", 20, 4)

    # Creating two layer model
    model = SequentialModel([layer, layer2])

    # Duplicating model
    model2 = SequentialModel(model.getStateList())
    # Setting model ones weights
    model2.setWeights(model.getWeights())

    # Checking if both outs generate the same value
    print (model2.compute(model.input_arr))
    model.mutate(25)
    print (model.compute())

