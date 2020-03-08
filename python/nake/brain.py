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



class BasicBrain(BrainBase):
    """ Basic brain """

    SEQUENTIALMODEL = "sequentialModel"

    def __init__(self, sequentialModel):
        if isinstance(sequentialModel, list):
            sequentialModel = SequentialModel(sequentialModel)
        assert isinstance(sequentialModel, SequentialModel)
        self.sequentialModel = sequentialModel

    @classmethod
    def create(cls, n_inputs=14, n_hidden_inputs=16, n_outputs=4):
        """ Sets up a basic brain class"""
        model = SequentialModel([
                    Dense("input_layer", n_inputs, n_hidden_inputs),
                    Dense("hidden_00", n_hidden_inputs, n_hidden_inputs),
                    Dense("hidden_01", n_hidden_inputs, n_hidden_inputs),
                    Dense("output_layer", n_hidden_inputs, n_outputs),
                         ])
        return cls(model)

    def crossover(self, brain2):
        """ Mixes two brains together"""
        pass

    def mutate(self, percent=5):
        """ Mutates a percentage of the non-locked networks weights """
        pass

    def __getstate__(self):
        """ Returns the state of the layer"""
        return {**super().__getstate__(), self.SEQUENTIALMODEL: self.sequentialModel.getStateList()}


    def computeMove(self, snake, board, food):
        """ Computes snakes move"""
        snake.moves2BoardEdges(board, moves=self.sequentialModel.input_arr[:4, 0])
        if food.isAvailable:
            self.sequentialModel.input_arr[4:6, 0] = food.pos - snake.headPosition
        else:
            self.sequentialModel.input_arr[4:6, 0] = 0
        snake.moves2Self(moves=self.sequentialModel.input_arr[6:14, 0])

        return self.sequentialModel.compute()





if __name__ == "__main__":

    brain = BasicBrain.create()
    brain2 = Brains(**brain.__getstate__())
    brain2.sequentialModel.compute()






