import utils
import numpy as np


class Board():

    def __init__(self, leftTop, rightBottom):
        if not len(leftTop)==2 or not len(rightBottom)==2:
            raise Exception("Incorrect input shapes")

        self.leftTop = leftTop
        self.rightBottom = rightBottom
        self.width = self.rightBottom[0]-self.leftTop[0]
        self.height = self.rightBottom[1]-self.leftTop[1]
        self.size = self.width*self.height
        self.shape = (self.height, self.width)

    @classmethod
    def fromDims(cls, width, height, *args, **kwargs):
        """ Initialize class from width and height"""
        return cls((0,0), (width, height), *args, **kwargs)

    def __str__(self):
        return "Lefttop {} rightBottom {}".format(self.leftTop, self.rightBottom)

    def __contains__(self, item):
        return self.pointInside(item)

    @property
    def x(self):
        return self.leftTop[0]

    @property
    def y(self):
        return self.leftTop[1]

    @property
    def x2(self):
        return self.rightBottom[0]

    @property
    def y2(self):
        return self.rightBottom[1]


    def movesToBoardEdges(self, point, moves=None):
        """ Returns the points number of moves to the edge of the board """
        return utils.moves2RectangleEdge(
            point, self.leftTop, self.rightBottom, moves=moves)

    def inside(self, point):
        """ Checks if the point is inside or outside the board """
        return point[0] >=  self.x and point[1] >= self.y and point[0] < self.x2 and point[1] < self.y2

    def outside(self, point):
        """ Checks if the point is outside or inside the board"""
        return self.inside(point) == False





if __name__ == "__main__":

    board = Board.fromDims(5, 5)
    print (board.width, board.height)
    print (board.movesToBoardEdges((3,3)))

    r = np.random.RandomState(1234)
    #ps = r.randint(199, size=1)

    r2 = np.random.RandomState()
    r2.set_state(r.get_state())
    ps = r2.randint(199, size=1)
    print (ps)