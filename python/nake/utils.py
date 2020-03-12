import numpy as np
import consts


def moves2Body(headPos, bodyPositions, angles=consts.ANGLES_45, moves=None):
    """ Returns number of moves to the head
        Angles in degrees, clockwise
        0 == Up
        90 == Right
        180 == Down
        270 == Left
    """
    if moves is None:
        moves = np.ones(len(angles), dtype=np.float32) * -1

    # Getting angle
    diff = (bodyPositions-headPos).astype(np.float32)

    ang = np.arctan2(diff[:, 1], diff[:, 0])+np.radians(90)
    val = np.rad2deg(ang % consts.PI2)

    dist = np.sqrt(diff[:, 0] ** 2 + diff[:, 1] ** 2)
    for idx, angle in enumerate(angles):
        idxs = np.where(val == angle)[0]
        if idxs.shape[0]:
            moves[idx] = np.min(dist[idxs])

    return moves


def moves2RectangleEdge(point, leftTop, rightBottom, moves=None):
    """ Returns the number of moves to the left, top, right, bottom edge"""
    if moves is None:
        moves = np.zeros(4,  dtype=np.float32)

    moves[0] = point[1]-leftTop[1]
    moves[1] = rightBottom[0]-point[0]-1
    moves[2] = rightBottom[1]-point[1]-1
    moves[3] = point[0] - leftTop[0]

    return moves



def checkRequiredKeys(data_dict, required_keys):
    """ Checks that all the required keys are in dict"""
    assert (isinstance(data_dict, dict))
    for rkey in required_keys:
        if not rkey in data_dict:
            raise KeyError("Required key \"{}\" is missing from input dict".format(rkey))



