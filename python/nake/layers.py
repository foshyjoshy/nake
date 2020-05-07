import numpy as np
from abc import abstractmethod
from registry import Registry, RegistryItemBase
from activations import Activation, Tanh, ActivationBase
import math



class SequentialModel():
    """ A list of layers that is computed sequential """

    LAYERS = 'layers'
    PREFIX = "sequential_model"

    def __init__(self, layers):
        for idx, layer in enumerate(layers):
            # Converting layer dict (getstate) to Layer objects
            if isinstance(layer, dict):
                layers[idx] = Layer(**layer)

        self.layers = layers
        self.input_arr = self.generateRandomInputs()

    @classmethod
    def fromState(cls, state, arrs=None):
        """ Initialize class from state """
        layers = state[cls.LAYERS]
        obj = cls([Layer(**layer) for layer in layers])
        if arrs is not None:
            obj.setArrs(arrs)
        return obj

    def __str__(self):
        return "SequentialModel({}x{}x{})".format(
            self.n_inputs, self.n_outputs, self.n_layers)

    def __iter__(self):
        for elem in self.layers:
            yield elem

    def __getitem__ (self, index):
        return self.layers[index]

    def __getstate__(self):
        return {self.LAYERS : [layer.__getstate__() for layer in self]}

    def layerByName(self, name):
        """ returns the layer for the given name"""
        for layer in self:
            if name == layer.name:
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

    def duplicate(self, duplicate_arrs=True):
        """ Duplicates class"""
        if duplicate_arrs:
            arrs = self.getArrs(copy=True)
        else:
            arrs = None
        return self.__class__.fromState(
            self.__getstate__(),
            arrs=arrs,
        )

    def generateRandomInputs(self, *args, **kwargs):
        """ Generate random inputs values for testing"""
        return self.layers[0].generateRandomInputs(*args, **kwargs)

    def compute(self, inputs=None):
        """ Runs the input values through the network"""
        if inputs is None: inputs = self.input_arr
        for layer in self.layers:
            inputs = layer.compute(inputs)
        return np.argmax(inputs)   #TODO add to class as config


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

    def getArrs(self, copy=False):
        """ return a dict of arrays used in model"""
        arrs = {}
        for layer in self:
            for key, arr in layer.getArrs().items():
                if copy:
                    arr = arr.copy()
                arrs["{}-{}-{}".format(self.PREFIX, layer.name, key)] = arr
        return arrs

    def setArrs(self, arrs):
        """" Sets a dict of arrays on layes"""
        for key, arr in arrs.items():
            layer_name, arr_name = key.split("-", 1)
            if layer_name == self.PREFIX:
                layer_name, arr_name = arr_name.split("-", 1)
            self.layerByName(layer_name).setArr(arr_name, arr)




class Layer(Registry):
    """ A class to store all layers"""
    registry = {}





class LayerBase(RegistryItemBase):
    """" Abstract base class for all layers to subclass """
    REGISTRY = Layer

    N_INPUTS = "n_inputs"
    N_OUTPUTS = "n_outputs"
    NAME = "name"
    ACTIVATION = "activation"
    USE_BIAS = "use_bias"
    STATE = "state"

    BIASES = "biases"
    WEIGHTS = "weights"


    def __init__(self, name):
        self.name = name


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

    @abstractmethod
    def getArrs(self):
        """ Returns this classes numpy arrays """

    @abstractmethod
    def setArr(self, arr_name, arr):
        """ Sets arr via name """


    def __getstate__(self):
        return {
            **super().__getstate__(),
            self.NAME: self.name,
        }





class Dense(LayerBase):
    """ Dense layer """

    def __init__(self, name, n_inputs, n_outputs, activation=None, use_bias=True, weights=None, biases=None):
        super().__init__(name)

        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.use_bias = use_bias

        if activation is None:
            activation = Activation.getInitialized("tanh")
        else:
            if not Activation.isObjectRegistered(activation):
                if isinstance(activation, dict):
                    activation = Activation(**activation)
                elif isinstance(activation, str):
                    activation = Activation(class_name=activation)
                else:
                    raise Exception("{} is not a "\
                    "registered activation. Use {}".format(activation, Activation.registeredClasses()))

        self.activation = activation


        if weights is None:
            # Between -1 and 1
            self.weights = (np.random.random((n_outputs, n_inputs)) * 2 - 1)
        else:
            assert isinstance(weights, np.ndarray)
            assert weights.shape == (n_outputs, n_inputs)
            self.weights = weights

        if biases is None:
            # Between -1 and 1
            self.biases = (np.random.random((n_outputs, 1)) * 2 - 1) * 0.001
        else:
            assert isinstance(biases, np.ndarray)
            assert biases.shape == (n_outputs, 1)
            self.biases = biases

        # Mutation mask ... create only once.
        self.mutation_mask = np.zeros_like(self.weights)


    def __str__(self):
        return "{}({}x{},use_bias={})".format(
            self.__class__.__name__, self.n_inputs, self.n_outputs, self.use_bias)

    def generateRandomInputs(self, minval=0, maxval=20):
        """ Generate random inputs values for testing"""
        return np.random.randint(minval, maxval, [self.n_inputs, 1])

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
            self.weights[indexes] = np.clip(self.weights[indexes] + (random_values*0.2), -1, 1)


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


    def __getstate__(self):
        return {
            **super().__getstate__(),
            self.ACTIVATION: self.activation.__getstate__(),
            self.N_INPUTS: self.n_inputs,
            self.N_OUTPUTS: self.n_outputs,
            self.NAME: self.name,
            self.USE_BIAS: self.use_bias,
        }

    def getArrs(self):
        """ Returns this classes numpy arrays """
        return {
            self.WEIGHTS: self.weights,
            self.BIASES: self.biases,
        }

    def setArr(self, arr_name, arr):
        """ Sets arr via name """
        if arr_name == self.WEIGHTS:
            self.setWeights(arr)
        elif arr_name == self.BIASES:
            self.setBiases(arr)
        else:
            raise Exception()








if __name__ == "__main__":



    layer = Layer("dense", "input_lay2er", 14, 16, use_bias=False, activation=Activation.getInitialized("relu"))
    layer2 = Layer("dense", "input_lay22er", 16, 16, activation=Activation.getInitialized("relu"))
    layer3 = Layer("dense", "input_lay222er", 16, 16, activation=Activation.getInitialized("relu"))
    layer4 = Layer("dense", "output_layer", 16, 4, activation=Activation.getInitialized("relu"))

    model = SequentialModel([layer, layer2, layer3, layer4])
    inputs = model.generateRandomInputs(-1, 1)

    np.savez_compressed(r"C:\tmp\sequence_test.npz", state=model.__getstate__(), **model.getArrs())


    #model2 = model.duplicate(True)
    #model3 = model.duplicate(True)
    #print (model.compute(inputs), model2.compute(inputs), model3.compute(inputs))



    #
    #
    # npz = np.load(r"C:\tmp\sequence_test.npz", allow_pickle=True)
    #
    # arr = dict([(key, value) for key, value in npz.items() if not key == "state"])
    #
    # state = npz["state"].item()
    #
    # model2 = SequentialModel.fromState(state,)
    #
    #
    # print (model.compute(inputs), model2.compute(inputs))
    #
    import os
    print (os.path.getsize(r"C:\tmp\sequence_test.npz")*1e-6, "mb")




