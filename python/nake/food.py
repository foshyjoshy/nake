import numpy as np



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

    def __repr__(self):
        return "Food({},{})".format(self.x, self.y)

    @property
    def shape(self):
        return self.board.shape

    @property
    def currentIndex(self):
        return self._currentIndex

    @currentIndex.setter
    def currentIndex(self, index):
        if index >= self._positions.shape[0]:
            self._generateNewPositions()
        else:
            self.setCurrentIndex(index)
        # Updating views for faster reading
        self.x = self._positions[self.currentIndex, 0]
        self.y = self._positions[self.currentIndex, 1]
        self.pos = self._positions[self.currentIndex]
        self.positions = self._positions[self.currentIndex:]


    def setCurrentIndex(self, idx=0):
        """ Sets the current index"""
        self._currentIndex = idx

    def prependPosition(self, pos):
        """ Prepends a positions to the start of the position arr"""
        self._positions = np.vstack([np.array(pos).reshape([-1, 2]), self._positions])
        if self.currentIndex > 0:
            self.currentIndex+=1

    def _generateNewPositions(self, resetindex=True):
        """ Generates new selfs.positions"""
        self._positions = np.vstack([
            self.randomStateX.randint(self.board.x, self.board.x2, size=self.nr),
            self.randomStateY.randint(self.board.y, self.board.y2, size=self.nr)
                ]).T
        if resetindex:
            self.currentIndex = 0

    def __eq__(self, other):
        return self.pos.__eq__(other)

    def __next__(self):
        self.next()
        return self.pos

    def next(self):
        """ Moves to next food position"""
        self.currentIndex+=1

    def findNext(self, positions, maxloop=-1):
        """ Makes sure the next position is not within the positions arr"""
        loopcount = 0
        while loopcount != maxloop:
            if not np.any(np.all(foodGen1.pos == positions, axis=1)):
                return True
            self.next()
            loopcount+=1
        return False






    # def __next__(self):
    #     """ Updates current position """
    #     self.




if __name__ == "__main__":

    from board import Board
    import time

    foodGen1 = FoodGenerator(Board.fromDims(128, 128), nr=100)

    positions = np.mgrid[0:128,0:128].T.reshape([-1, 2])
    np.random.shuffle(positions)
    positions = positions[:128*128-1]

    print (positions.shape)
    print (np.multiply(*foodGen1.shape))

    a = time.time()
    status = foodGen1.findNext(positions, maxloop=-1)
    print (status)
    print (time.time()-a)