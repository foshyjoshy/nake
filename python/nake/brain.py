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






class BasicBrain(BrainBase):
    """ Basic brain """

    SEQUENTIAL_MODEL = "sequential_model"

    def __init__(self, sequential_model, *args, **kwargs):
        if isinstance(sequential_model, list):
            sequential_model = SequentialModel(sequential_model)
        assert isinstance(sequential_model, SequentialModel)

        self.sequential_model = sequential_model
        super().__init__(*args, **kwargs)

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
        """ Mutates a percentage of the non-locked networks weights """
        pass

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





if __name__ == "__main__":

    brain = BasicBrain.create(name="s")
    brain2 = Brains(**brain.__getstate__())
    brain2.sequential_model.compute()

    print (brain2.__getstate__())

    computeMove

