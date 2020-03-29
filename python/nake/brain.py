from registry import Registry, RegistryItemBase
from abc import abstractmethod
from layers import SequentialModel, Dense
import consts



class Brains(Registry):
    """ A class to store all brains"""
    registry = {}


class BrainBase(RegistryItemBase):
    """ Base class for Brains """
    REGISTRY = Brains

    NAME = "name"

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "name={}".format(self.name)

    def __repr__(self):
        return self.name

    @abstractmethod
    def crossover(self, brain2):
        """ Mixes two brains together"""
        pass

    @abstractmethod
    def mutate(self, percent=5):
        """ Mutates a percentage of the non-locked networks weights """
        pass

    @abstractmethod
    def computeMove(self, snake, board, food):
        """ Computes snakes move"""

    def __getstate__(self):
        """ Returns the state of the brain"""
        return {**super().__getstate__(),self.NAME : self.name}

    def duplicate(self, name=None):
        """ Duplicate object """
        state = self.__getstate__()
        if name is not None:
            state[self.NAME] = name
        return Brains.getInitialized(**state)






class BasicBrain(BrainBase):
    """ Basic brain """

    SEQUENTIAL_MODEL = "sequential_model"

    def __init__(self, sequential_model, *args, **kwargs):
        if isinstance(sequential_model, list):
            sequential_model = SequentialModel(sequential_model)
        assert isinstance(sequential_model, SequentialModel)

        self.sequential_model = sequential_model
        super().__init__(*args, **kwargs)


    def __str__(self):
        return "{} {}".format(super().__str__(), self.sequential_model)

    @classmethod
    def create(cls, n_inputs=14, n_hidden_inputs=16, n_outputs=4, **kwargs):
        """ Sets up a basic brain class"""
        sequential_model = SequentialModel([
                    Dense("input_layer", n_inputs, n_hidden_inputs),
                    Dense("hidden_00", n_hidden_inputs, n_hidden_inputs),
                    Dense("hidden_01", n_hidden_inputs, n_hidden_inputs),
                    Dense("output_layer", n_hidden_inputs, n_outputs),
                         ])
        return cls(sequential_model,**kwargs)

    def crossover(self, brain2):
        """ Mixes two brains together"""
        pass

    def mutate(self, percent=5):
        """ Runs sequential model mutation"""
        self.sequential_model.mutate(percent=percent)

    def __getstate__(self):
        """ Returns the state of the brain"""
        return {
            **super().__getstate__(),
            self.SEQUENTIAL_MODEL: self.sequential_model.getStateList(),
                }


    def computeMove(self, snake, board, food):
        """ Computes snakes move"""
        snake.moves2BoardEdges(board, moves=self.sequential_model.input_arr[:4, 0])
        if food.isAvailable:
            self.sequential_model.input_arr[4:6, 0] = food.pos - snake.headPosition
        else:
            self.sequential_model.input_arr[4:6, 0] = 0
        snake.moves2Self(moves=self.sequential_model.input_arr[6:14, 0])
        return self.sequential_model.compute()


    def duplicate(self, *args, weights=True, **kwargs):
        """ Duplicate object """
        brain = super().duplicate(*args, **kwargs)
        if weights:
            brain.sequential_model.setWeights(self.sequential_model.getWeights())
        return brain





if __name__ == "__main__":

    brain = BasicBrain.create(name="s")
    brain2 = Brains(**brain.__getstate__())
    brain2.sequential_model.compute()

    print (brain2.__getstate__())

    computeMove

