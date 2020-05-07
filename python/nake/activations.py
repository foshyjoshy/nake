import numpy as np
from registry import Registry, RegistryItemBase
from abc import abstractmethod


class Activation(Registry):
    """ A class to store all activations """
    registry = {}


class ActivationBase(RegistryItemBase):
    """ Base class for Activations """
    REGISTRY = Activation

    GROUP_NAME = "activation"

    @abstractmethod
    def compute(self, x, out=None):
        pass



class Tanh(ActivationBase):
    """ hyperbolic tangent function """

    def compute(self, x, out=None):
        return np.tanh(x, out=out)


class Relu(ActivationBase):
    """ rectified linear unit """

    def compute(self, x, out=None):
        return np.maximum(x, 0, out=out)

class LeakyRelu(ActivationBase):
    """ leaky rectified linear unit """
    def compute(self, x, out=None):
        _out = np.where(x > 0, x, x * 0.01)
        if out is not None:
            out[:] = _out
        else:
            out = _out
        return out



if __name__ == "__main__":


    import h5py

    # Create activation
    act = Activation.getInitialized("tanh")
    act2 = Activation.getInitialized("relu")
    act3 = Activation.getInitialized("leakyrelu")

    print (act3.compute(np.arange(10)-5))









