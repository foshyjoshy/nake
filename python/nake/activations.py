import numpy as np
from abc import ABC, abstractmethod
from logging import debug
import consts
from registry import Registry


class Activations(Registry):
    """ A class to store all activations """



class ActivationBase(ABC):
    """" Abstract base class for activations """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Activations.register(cls)

    @classmethod
    def getName(cls):
        """ Returns the name of the activation"""
        return cls.__name__.lower()

    @abstractmethod
    def compute(self, value):
        pass

    def getState(self):
        """ Returns the state of this object """
        return {consts.NAME : self.getName()}



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
            return {**super().getState(), "a" : self.a}

    import json

    act = Activations.getInitialized("testclass", a=10, b=2)
    act.compute(act)
    dump = json.dumps(act.getState())
    #
    # act = Activations.getInitialized("relu")
    # print (act.compute(np.arange(-10, 10)))
    # state =  act.getState()

    act = Activations(**act.getState())
    print (act.compute("s"))






