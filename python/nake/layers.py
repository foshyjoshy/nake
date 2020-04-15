import numpy as np
from abc import abstractmethod
from registry import Registry, RegistryItemBase
from activations import Activation, Tanh, ActivationBase
from logging import debug
import math
import json
import h5py


class SequentialModel():
    """ A list of layers that is computed sequential """

    LAYER_ORDER = "layer_order"
    LAYER_NAMES = "LAYER_{:04d}"


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

    def setDataOnGroup(self, grp):
        """ Sets classes data the h5py grp"""
        assert isinstance(grp, h5py.Group)
        for lidx, layer in enumerate(self):
            layer_grp = grp.create_group(self.LAYER_NAMES.format(lidx))
            layer.setDataOnGroup(layer_grp)

    @classmethod
    def fromGroup(cls, grp):
        """ Initialized via h5py group"""
        layers = []
        for lidx in range(len(grp)):
            layer_name = cls.LAYER_NAMES.format(lidx)
            layer = Layer(grp.get(layer_name))
            if layer is None:
                break
            else:
                layers.append(layer)
        return cls(layers)











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
    STATE = "state"

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

    def __init__(self, layer_name, n_inputs, n_outputs, activation=None, use_bias=True, weights=None, biases=None):
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



    def setDataOnGroup(self, grp, set_arrays=True):
        """ Sets classes data the h5py grp"""
        super().setDataOnGroup(grp)

        # Dumping state to json string for writing
        state = {
            self.N_INPUTS: self.n_inputs,
            self.N_OUTPUTS: self.n_outputs,
            self.LAYER_NAME: self.layer_name,
            self.USE_BIAS: self.use_bias,
        }
        grp.attrs[self.STATE] = json.dumps(state)

        if set_arrays:
            # Creating datasets for numpy arrays
            grp.create_dataset(self.WEIGHTS, data=self.weights)
            grp.create_dataset(self.BIASES, data=self.biases)

        # Adding activation to grp
        self.activation.setDataOnGroup(grp.create_group(ActivationBase.GROUP_NAME))

    @classmethod
    def fromGroup(cls, grp):
        """ Initialized via h5py group"""

        weights = grp.get(cls.WEIGHTS)
        if weights is not None:
            weights = weights[:]

        biases = grp.get(cls.BIASES)
        if biases is not None:
            biases = biases[:]

        activation = Activation(grp.get(ActivationBase.GROUP_NAME))

        state = json.loads(grp.attrs[cls.STATE])

        return cls(
            state[cls.LAYER_NAME], state[cls.N_INPUTS], state[cls.N_OUTPUTS],
            use_bias=state.get(cls.USE_BIAS),
            weights=weights,
            biases=biases,
            activation=activation,
        )




if __name__ == "__main__":



    # path = r"C:\tmp\layer_test.hdf5"
    # with h5py.File(path, "w") as FILE:
    #     layer = Layer("dense", "input_layer", 21, 4, activation = Activation.getInitialized("relu"))
    #     layer.setDataOnGroup(FILE.create_group("input_layer"))
    #
    # with h5py.File(path, "r") as FILE:
    #     layer2 = Layer(FILE.get("input_layer"))
    #
    # inputs = layer.generateRandomInputs(-2,21)
    # assert np.all(layer.compute(inputs.copy()) == layer2.compute(inputs.copy()))
    #

    path = r"C:\tmp\sequence_test.hdf5"
    with h5py.File(path, "w") as FILE:
        layer = Layer("dense", "input_layer", 14, 16, activation = Activation.getInitialized("relu"))
        layer2 = Layer("dense", "input_layer", 16, 16, activation=Activation.getInitialized("relu"))
        layer3 = Layer("dense", "input_layer", 16, 16, activation=Activation.getInitialized("relu"))
        layer4 = Layer("dense", "output_layer", 16, 4, activation=Activation.getInitialized("relu"))

        for i in range(10000):
            model = SequentialModel([layer, layer2, layer3, layer4])
            model.setDataOnGroup(FILE.create_group("model_{}".format(i)))
    #
    # with h5py.File(path, "r") as FILE:
    #     model2 = SequentialModel.fromGroup(FILE.get("model"))
    #
    # inputs = model.generateRandomInputs(-2,21)
    # print (model.compute(inputs))
    # print (model2.compute(inputs))

