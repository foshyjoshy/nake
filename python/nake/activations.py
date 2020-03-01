import numpy as np
from abc import ABC, abstractmethod
from logging import debug
import consts



class Activations():
    """ A class to store all activations """

    registry = {}


    def __new__(cls, **kwargs):
        return cls.getInitialized(kwargs.pop(consts.NAME,None), **kwargs)

    @classmethod
    def isRegistered(cls, obj):
        """ Checks if the obj is registered"""
        return obj in cls.registry.items()

    @classmethod
    def isNameRegistered(cls, name):
        """" Checks if a name is in the registry"""
        return name in cls.registry

    @classmethod
    def register(cls, act):
        """" Register an activation"""
        if not issubclass(act, ActivationBase):
            raise Exception("Unable to register {}. \
                Not a subclass of {}".format(act, ActivationBase))
        if cls.isNameRegistered(act.getName()):
            raise Exception("Unable to register {}. \
                {} is already registered".format(act, act.getName()))

        debug("Registered class {} with name {}".format(act, act.getName()))
        cls.registry[act.getName()] = act

    @classmethod
    def get(cls, name, value=None):
        """ Returns registered activation with name"""
        return cls.registry.get(name, value)

    @classmethod
    def getInitialized(cls, name, *args, **kwargs):
        """ Returns registered initialized activation with name"""
        if cls.isNameRegistered(name):
            return cls.get(name)(*args, **kwargs)
        else:
            Exception("Nothing has been registered with name \"{}\"".format(name))




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






