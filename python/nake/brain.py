from registry import Registry, RegistryItemBase
from abc import abstractmethod
from layers import SequentialModel, Dense
import copy
import numpy as np



class Brains(Registry):
    """ A class to store all brains"""
    registry = {}

    @classmethod
    def fromState(cls, state, arrs=None):
        """ Initialize class from state """
        class_name = state.pop(Brains.CLASS_NAME)
        if not cls.isNameRegistered(class_name):
            raise Exception("Nothing has been registered \
                   with name \"{}\". Available {}".format(class_name, cls.registry))
        return cls.get(class_name).fromState(state, arrs=arrs)

    @classmethod
    def load(cls, filepath, name=None):
        """ Loads brain from npz filepath"""
        npfile = np.load(filepath, allow_pickle=True)
        arrs = dict(npfile.items())
        state = arrs.pop(BrainBase.STATE).item()
        if name is not None:
            state[BrainBase.NAME] = name
        return cls.fromState(state, arrs=arrs)




class BrainBase(RegistryItemBase):
    """ Base class for Brains """
    REGISTRY = Brains

    NAME = "name"
    STATE = "state"

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "name={}".format(self.name)

    def __repr__(self):
        return self.name


    @classmethod
    @abstractmethod
    def fromState(cls, state, arrs=None):
        """ Initialize class from state """

    def save(self, filepath, compressed=False):
        """ Writes brain to npz """
        arrs = self.getArrs()
        if self.STATE in arrs.keys():
            raise Exception("{} is an invalid key for self.getAttrs()".format(self.STATE))
        else:
            arrs[self.STATE] =  self.__getstate__()
        return (np.savez_compressed if compressed else np.savez)(filepath,**arrs)

    @abstractmethod
    def mutate(self, rate=5):
        """ Mutates a percentage of the non-locked networks weights """
        pass

    @abstractmethod
    def crossover(self, brain2):
        """ Mixes two brains together"""
        pass

    @abstractmethod
    def isCrossCompatible(self, other):
        """ Checks if other brain is cross compatible"""

    @abstractmethod
    def computeMove(self, snake, board, food):
        """ Computes snakes move"""

    @abstractmethod
    def getArrs(self):
        """ Returns a dict of numpy arrays for saving"""

    @abstractmethod
    def setArrs(self, arrs):
        """ Sets the input arrays on the brain """

    def __getstate__(self):
        """ Returns the state of the brain"""
        return {**super().__getstate__(),self.NAME : self.name}

    def duplicate(self, name=None, duplicate_arrs=True):
        """ Duplicates class """
        state = self.__getstate__()
        if name is not None:
            state[self.NAME] = name
        if duplicate_arrs:
            arrs = self.getArrs(copy=True)
        else:
            arrs = None
        return self.__class__.fromState(state, arrs=arrs)




class BasicBrain(BrainBase):
    """ Basic brain """

    SEQUENTIAL_MODEL = "sequential_model"

    def __init__(self, sequential_model, *args, **kwargs):
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

    @classmethod
    def fromState(cls, state, arrs=None):
        """ Initialize class from state """
        class_name = state.pop(Brains.CLASS_NAME, None)
        if class_name is not None:
            if not cls.getClassName() == class_name:
                raise Exception("States class_name {} is does not match {}".format(
                    class_name, cls.getClassName()
                ))

        model_state = state.pop(cls.SEQUENTIAL_MODEL)
        model = SequentialModel.fromState(model_state, arrs=arrs)
        return cls(model, **state)


    def isCrossCompatible(self, other):
        """ Checks if other brain is cross compatible"""
        return isinstance(other, BasicBrain)

    def crossover(self, *others):
        """ Mixes brains together """
        for other in others:
            if not self.isCrossCompatible(other):
                raise Exception("Unable to crossover {} with {}".format(other, self))
        if not len(others):
            raise Exception("Why are you trying to crossover with nothing?")
        return self.sequential_model.crossover(*[other.sequential_model for other in others])

    def mutate(self, rate=5):
        """ Runs sequential model mutation"""
        return self.sequential_model.mutate(percent=rate)

    def getArrs(self, copy=False):
        """ Returns a dict of numpy arrays for saving"""
        return self.sequential_model.getArrs(copy=copy)

    def setArrs(self, arrs):
        """ Sets the input arrays on the brain """
        self.sequential_model.setArrs(arrs)

    def __getstate__(self):
        """ Returns the state of the brain"""
        return {
            **super().__getstate__(),
            self.SEQUENTIAL_MODEL: copy.deepcopy(self.sequential_model.__getstate__()),
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





def crossover(name, *brains):
    """ Runs a cross over of the input brains """
    if  len(brains) < 2:
        raise Exception("Unable to run cross over with less that 2 brains")
    new_brain = brains[0].duplicate(name=name, duplicate_arrs=True)
    new_brain.crossover(*brains[1:])
    return new_brain




class BrainGenerators(Registry):
    """ A class where we store all the brain generators"""
    registry = {}



class BrainGeneratorBase(RegistryItemBase):
    """ Base class for BrainGenerators """
    REGISTRY = BrainGenerators

    DEFAULT_N_GENERATE = 10
    DEFAULT_MUTATE_RATE = 5
    DEFAULT_BRAIN_NAME = "brain_{idx:09d}"

    BRAIN_NAME = "brain_name"
    N_GENERATE = "n_generate"
    MUTATE_RATE = "mutate_rate"


    def __init__(self, n_generate=None, brain_name=None):
        self.brain_name = brain_name or self.DEFAULT_BRAIN_NAME
        self.n_generate = n_generate or self.DEFAULT_N_GENERATE
        self.n_generated = 0

    def __iter__(self):
        self.n_generated = 0
        return self

    def __next__(self):
        if self.n_generated >= self.n_generate:
            raise StopIteration
        self.n_generated += 1
        return self.generate(self.n_generated-1)

    def __getstate__(self):
        """ Returns the of the generator"""
        return {
            **super().__getstate__(),
            self.N_GENERATE: self.n_generate,
            self.BRAIN_NAME: self.brain_name,
                }

    def generatename(self, idx):
        return self.brain_name.format(idx=idx)

    @abstractmethod
    def generate(self, idx):
        """  generates and returns new brain"""
        pass



class BasicBrainGenerator(BrainGeneratorBase):
    """ Duplicates input brain without weights"""

    def __init__(self, brain, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not Brains.isObjectRegistered(brain):
            raise Exception("{} is not a registered brain" \
                "registered activation. Use {}".format(brain, Brains.registeredClasses()))
        self.brain = brain

    def generate(self, idx):
        """  generates and returns new brain"""
        return self.brain.duplicate(
                        name=self.generatename(idx),
                        duplicate_arrs=False
                        )



class CrossoverBrainGenerator(BrainGeneratorBase):
    """Crossovers input brains"""

    def __init__(self, brains, *args, mutate_rate=None, **kwargs):
        super().__init__(*args, **kwargs)

        for idx, brain in enumerate(brains):
            if not Brains.isObjectRegistered(brains[idx]):
                raise Exception("{} is not a registered brain" \
                                "registered activation. Use {}".format(brains[idx], Brains.registeredClasses()))

        self.mutate_rate = mutate_rate or self.DEFAULT_MUTATE_RATE
        self.brains = brains

    def generate(self, idx):
        """  generates and returns new brain"""
        brain = crossover(self.generatename(idx), *self.brains)
        if self.mutate_rate:
            brain.mutate(rate=self.mutate_rate)
        return brain










if __name__ == "__main__":

    from snake import Snake
    from board import Board
    from food import FoodGenerator
    import consts

    board = Board.fromDims(10, 10)
    food = FoodGenerator(board, (1, 1), 2321)
    snake = Snake.initializeAtPosition((5, 5), direction=consts.Moves.DOWN, name="loop")


    path = r"C:\tmp\brain_test.npz"
    brain1 = BasicBrain.create(name="brain1")
    brain2 = brain1.duplicate(name="brain2")
    brain1.save(path, compressed=True)
    brain3 = Brains.load(path, name="brain3")

    print (brain1, brain1.computeMove(snake, board, food))
    print (brain2, brain2.computeMove(snake, board, food))
    print (brain3, brain3.computeMove(snake, board, food))

    import os
    print (os.path.getsize(path)*1e-6, "mb")

    gen = BasicBrainGenerator(brain1, n_generate=4)
    for brain in gen:
        print (brain, brain.computeMove(snake, board, food))

    print ("\n")

    brain1.sequential_model[0].weights[:] = 0
    brain2.sequential_model[0].weights[:] = 1
    brain3.sequential_model[0].weights[:] = 2
    gen = CrossoverBrainGenerator([brain1, brain2, brain3], n_generate=4)
    for brain in gen:
        print (brain.sequential_model[0].weights[:5,0])
        print (brain, brain.computeMove(snake, board, food))


