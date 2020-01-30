import numpy as np
from logging import debug


def foodGenerator(board, seed=None, num=9999):
    """ Generates food intill the end of days"""
    randomState = np.random.RandomState(seed=seed)

    xs = randomState.randint(board.x, board.x2, size=num)
    ys = randomState.randint(board.y, board.y2, size=num)
    positions = np.vstack([xs, ys])

    idx = 0
    while idx < positions.shape[0]:
        yield positions[idx]



class FoodGenerator():
    """ Handles the snakes food random state"""

    DEFAULT_NRPOSITIONS = 999

    def __init__(self, board, pos=None, stateX=None, stateY=None, seedX=None, seedY=None, nr=None):
        self.randomStateX = np.random.RandomState(seed=seedX)
        self.randomStateY = np.random.RandomState(seed=seedY)
        if stateX is not None:
            self.randomStateX.set_state(stateX)
        if stateY is not None:
            self.randomStateY.set_state(stateY)

        self.stateX = self.randomStateX.get_state()
        self.stateY = self.randomStateY.get_state()
        self.board = board
        self.nr = nr or self.DEFAULT_NRPOSITIONS

        # Generating positions
        self._generateNewPositions()
        if pos is not None:
            self.prependPosition(pos)

    def __str__(self):
        return "Food {} {} index {}".format(self.x, self.y, self.currentIndex)

    @property
    def currentIndex(self):
        return self._currentIndex

    @currentIndex.setter
    def currentIndex(self, index):
        if index >= self.positions.shape[0]:
            self._generateNewPositions()
        else:
            self.setCurrentIndex(index)
        # Updating views for faster reading
        self.x = self.positions[self.currentIndex, 0]
        self.y = self.positions[self.currentIndex, 1]
        self.pos = self.positions[self.currentIndex]

    def next(self):
        """ Moves to next food position"""
        self.currentIndex+=1

    def setCurrentIndex(self, idx=0):
        """ Sets the current index"""
        self._currentIndex = idx

    def prependPosition(self, pos):
        """ Prepends a positions to the start of the position arr"""
        self.positions = np.vstack([np.array(pos).reshape([-1, 2]), self.positions])
        if self.currentIndex > 0:
            self.currentIndex+=1

    def _generateNewPositions(self, resetindex=True):
        """ Generates new selfs.positions"""
        self.positions = np.vstack([
            self.randomStateX.randint(self.board.x, self.board.x2, size=self.nr),
            self.randomStateY.randint(self.board.y, self.board.y2, size=self.nr)
                ]).T
        if resetindex:
            self.currentIndex = 0







    # def __next__(self):
    #     """ Updates current position """
    #     self.




if __name__ == "__main__":

    from board import Board
    import time

    foodGen1 = FoodGenerator(Board.fromDims(64, 64), (20,20), nr=2)
    foodGen2 = FoodGenerator(Board.fromDims(64, 64), (20, 20), nr=10, stateX=foodGen1.stateX, stateY=foodGen1.stateY)
    for i in range(100):
        foodGen1.next()
        foodGen2.next()
        print (foodGen1, foodGen2)



