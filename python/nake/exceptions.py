import consts


class InvalidDirection(Exception):
    """When we hit an invalid direction"""
    def __init__(self, direction):
        super().__init__("Invalid direction \"{}\"... valid directions are {} ".format(
            direction,
            consts.DISTANCES_STR,
        ))
        self.direction = direction

class InvalidMove(Exception):
    """ When a move is invalid """
    def __init__(self, direction, validmoves=None):
        if validmoves is None:
            validmoves = consts.VALID_MOVEMENTS[direction]
        super().__init__("Unable to move {}. Valid movements are {}".format(
            direction,
            validmoves
        ))
        self.direction = direction

class OutsideBoard(Exception):
    """Raise for my specific kind of exception"""