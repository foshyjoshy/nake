import numpy as np
from enum import Enum
from functools import partial



def relu(x, out=None):
    """ rectified linear unit """
    return np.maximum(x,0, out=out)



class Activations(Enum):
    """ Enum used to store available activations"""

    TANH = np.tanh
    RELU = partial(relu)


    def __init__(self, *args):
        cls = self.__class__
        # Making sure the lower of name doesn't already exist
        if cls.hasActivation(self.name):
            raise ValueError("cls {} names lower and upper matches not allowed".format(cls.__name__))

    def __str__(self):
        return self.name.lower()

    @classmethod
    def memberNames(cls):
        return set(cls._member_names_ + [name.lower() for name in cls._member_names_])

    @classmethod
    def hasActivation(cls, value):
        """ Checks to see if the activation functions exists in the """
        return value in cls.memberNames()

    def compute(self, *args, **kwargs):
        """ Computes the activations function"""
        return self.value( *args, **kwargs)





if __name__ == "__main__":

    print (Activations.hasActivation("TANH"))
    a = np.arange(-10, 100)
    activation = Activations.TANH
    r = activation.compute(a)
    print (r)