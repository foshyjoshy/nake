import numpy as np
from registry import Registry, RegistryItemBase
from abc import abstractmethod


class Activation(Registry):
    """ A class to store all activations """
    registry = {}


class ActivationBase(RegistryItemBase):
    """ Base class for Activations """
    REGISTRY = Activation

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

    class TestClass(ActivationBase):
        """ Test class """

        def __init__(self, a, b=None):
            self.a = a
            self.b = b

        def compute(self, x, out=None):
            return ("test", self.a, self.b)

        def getState(self):
            return {**super().getState(), "a": self.a}


    print ("Available activations {}".format(Activation.registeredNames()))
    act = Activation.getInitialized("tanh")
    print ("Tanh of 1", act.compute(1))
    act = Activation.getInitialized("testclass", a="test")
    act.compute(act)
    print (act.getState())
    act = Activation(**act.getState())
    act.compute("s")










