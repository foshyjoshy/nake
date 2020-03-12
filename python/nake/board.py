import utils
import numpy as np


class Board():

    LEFT_TOP = "left_top"
    RIGHT_BOTTOM = "right_bottom"

    DEFAULT_LEFT_TOP = (0,0)

    def __init__(self, leftTop, rightBottom):

        self.leftTop = np.array(leftTop, dtype=int)
        self.rightBottom = np.array(rightBottom, dtype=int)
        if not self.leftTop.shape == (2,) or not self.rightBottom.shape == (2,):
           raise Exception("Incorrect input shapes. Shape of (2,) required")


        self.width = self.rightBottom[0]-self.leftTop[0]
        self.height = self.rightBottom[1]-self.leftTop[1]
        self.size = self.width*self.height
        self.shape = (self.height, self.width)

    @classmethod
    def fromDims(cls, width, height, *args, **kwargs):
        """ Initialize class from width and height"""
        return cls((0,0), (width, height), *args, **kwargs)

    @classmethod
    def fromState(cls, stateDict):
        """ Initialize from state"""
        utils.checkRequiredKeys(stateDict, [cls.RIGHT_BOTTOM])
        return cls(
            stateDict.get(cls.LEFT_TOP, cls.DEFAULT_LEFT_TOP),
            stateDict.get(cls.RIGHT_BOTTOM),
        )

    def __getstate__(self):
        """ Returns the state of the board"""
        return {
            self.LEFT_TOP : self.leftTop.tolist(),
            self.RIGHT_BOTTOM : self.rightBottom.tolist(),
        }

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
    print (board.__getstate__())

    board2 = Board.fromState(board.__getstate__())