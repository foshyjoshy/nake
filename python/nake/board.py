import utils


class Board():

    def __init__(self, leftTop, rightBottom):
        if not len(leftTop)==2 or not len(rightBottom)==2:
            raise Exception("Incorrect input shapes")

        self.leftTop = leftTop
        self.rightBottom = rightBottom

    @classmethod
    def fromDims(cls, width, height, *args, **kwargs):
        """ Initialize class from width and height"""
        return cls((0,0), (width, height), *args, **kwargs)

    def __str__(self):
        return "Lefttop {} rightBottom {}".format(self.leftTop, self.rightBottom)

    @property
    def x(self):
        return self.leftTop[0]

    @property
    def y(self):
        return self.leftTop[1]

    @property
    def width(self):
        return self.rightBottom[0]-self.leftTop[0]

    @property
    def height(self):
        return self.rightBottom[1]-self.leftTop[1]

    def movesToBoardEdges(self, point, moves=None):
        """ Returns the points number of moves to the edge of the board """
        return utils.moves2RectangleEdge(
            point, self.leftTop, self.rightBottom, moves=moves)




if __name__ == "__main__":

    board = Board.fromDims(5, 5)
    print (board.width, board.height)
    print (board.getDistanceToBoardEdges((3,3)))

