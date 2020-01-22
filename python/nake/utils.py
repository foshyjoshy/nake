import numpy as np
import consts


def distance2Body(headPos, bodyPositions, angles=consts.ANGLES_45, distances=None):
    """ Returns the distance to head
        0 == Right
        90 == Down
        180 == Left
        270 == Up
    """
    if distances is None:
        distances = np.ones(len(angles), dtype=np.float32) * -1

    # Getting angle
    diff = (bodyPositions-headPos).astype(np.float32)

    ang = np.arctan2(diff[:, 0], diff[:, 1])
    val = np.rad2deg(ang % consts.PI2)

    dist = np.sqrt(diff[:, 0] ** 2 + diff[:, 1] ** 2)
    for idx, angle in enumerate(angles):
        idxs = np.where(val == angle)[0]
        if idxs.shape[0]:
            distances[idx] = np.min(dist[idxs])

    return distances


def distance2RectangleEdge(point, leftTop, rightBottom, distances=None):
    """ Returns the distance to the left, top, right, bottom edge"""
    if distances is None:
        distances = np.zeros(4,  dtype=np.float32)

    distances[0] = point[0]-leftTop[0]
    distances[1] = point[1]-leftTop[1]
    distances[2] = rightBottom[0]-point[0]-1
    distances[3] = rightBottom[1]-point[1]-1

    return distances