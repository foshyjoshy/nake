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
        return np.maximum(x,0, out=out)








if __name__ == "__main__":


    import h5py

    # Create activation
    act = Activation.getInitialized("tanh")
    act2 = Activation.getInitialized("relu")

    path = r"C:\tmp\activation_test.hdf5"

    with h5py.File(path, "w") as FILE:
        act.setDataOnGroup(FILE.create_group("activation"))
        act2.setDataOnGroup(FILE.create_group("activation2"))

    with h5py.File(path, "r") as FILE:
        print (Activation(FILE.get("activation")))
        print(Activation(FILE.get("activation2")))









