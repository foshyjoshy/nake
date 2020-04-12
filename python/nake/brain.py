from registry import Registry, RegistryItemBase
from abc import abstractmethod
from layers import SequentialModel, Dense
import copy
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


    def getArrs(self):
        """ Returns a dict of numpy arrays for saving"""
        return dict([("{}_{}".format(self.name, key), arr) for key, arr
                in self.sequential_model.getWeights().items()])

    def setArrs(self, arrs):
        """ Sets the input arrays on the brain """
        raise NotImplemented()


    def __getstate__(self):
        """ Returns the state of the brain"""
        return {
            **super().__getstate__(),
            self.SEQUENTIAL_MODEL: copy.deepcopy(self.sequential_model.getStateList()),
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

    def duplicate(self, *args, weights=True, weights_copy=True, **kwargs):
        """ Duplicate object """
        brain = super().duplicate(*args, **kwargs)
        if weights:
            brain.sequential_model.setWeights(self.sequential_model.getWeights(return_copy=weights_copy))
        return brain





def crossover(name, *brains):
    """ Runs a cross over of the input brains """
    if  len(brains) < 2:
        raise Exception("Unable to run cross over with less that 2 brains")
    new_brain = brains[0].duplicate(name, weights=True,weights_copy=True )
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

    BRAIN = "brain"
    N_GENERATE = "n_generate"
    MUTATE_RATE = "mutate_rate"

    def __init__(self, n_generate=None):
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
                }

    @abstractmethod
    def generate(self, idx):
        """  generates and returns new brain"""
        pass



class BasicBrainGenerator(BrainGeneratorBase):
    """ Duplicates input brain without weights"""

    def __init__(self, brain, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(brain, dict):
            brain = Brains.getInitialized(**brain)

        if not Brains.isObjectRegistered(brain):
            raise Exception("{} is not a registered brain" \
                "registered activation. Use {}".format(brain, Brains.registeredClasses()))
        self.brain = brain

    def generate(self, idx):
        """  generates and returns new brain"""
        return self.brain.duplicate(weights=False, weights_copy=False)



#TODO Add name to generate functions

class CrossoverBrainGenerator(BrainGeneratorBase):
    """Crossovers input brains"""

    def __init__(self, brains, *args, mutate_rate=None, **kwargs):
        super().__init__(*args, **kwargs)

        for idx, brain in enumerate(brains):
            # Converting brain dict (getstate) to Brain objects
            if isinstance(brain, dict):
                brains[idx] = Brains(**brain)
            if not Brains.isObjectRegistered(brains[idx]):
                raise Exception("{} is not a registered brain" \
                                "registered activation. Use {}".format(brains[idx], Brains.registeredClasses()))

        self.mutate_rate = mutate_rate or self.DEFAULT_MUTATE_RATE
        self.brains = brains

    def generate(self, idx):
        """  generates and returns new brain"""
        brain = crossover("ss", *self.brains)
        if self.mutate_rate:
            brain.mutate(rate=self.mutate_rate)
        return brain












if __name__ == "__main__":


    import time


    b1 = BasicBrain.create(name="b1")
    b2 = BasicBrain.create(name="b2")

    gen = CrossoverBrainGenerator([b1, b2], n_generate=1000)
    gen = BasicBrainGenerator(b1, n_generate=1000)

    a = time.time()
    for i in gen:
        #print (i)
        pass
    print( time.time()-a)




