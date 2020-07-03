import numpy as np
import consts

OFFSETS = np.array([[
    [0.5, 0.5],
    [-0.5, 0.5],
    [-0.5, -0.5],
    [0.5, -0.5]
    ]]
)


def moves2Body(headPos, bodyPositions, angles=consts.ANGLES_45, moves=None, default_value=None):
    """ Returns number of moves to the head
        Angles in degrees, clockwise
        0 == Up
        90 == Right
        180 == Down
        270 == Left
    """
    if default_value is None:
        default_value = -1
    if moves is None:
        moves = np.zeros(len(angles), dtype=np.float32)

    # Getting angle
    diff = (bodyPositions-headPos).astype(np.float32)

    ang = np.arctan2(diff[:, 1], diff[:, 0])+np.radians(90)
    val = np.rad2deg(ang % consts.PI2)

    dist = np.sqrt(diff[:, 0] ** 2 + diff[:, 1] ** 2)
    for idx, angle in enumerate(angles):
        idxs = np.where(val == angle)[0]
        if idxs.shape[0]:
            moves[idx] = np.min(dist[idxs])
        else:
            moves[idx] = default_value

    return moves


def radar_angles( head_pos, body_positions, default_value=None):
    """ """
    if default_value is None:
        default_value = -1

    # Getting difference between body and head position
    diff = (body_positions-head_pos).astype(np.float32)

    arr = (np.repeat(OFFSETS, len(diff), axis=0))
    arr += diff.reshape([-1, 1,2])

    # Getting all array angles
    ang = np.arctan2(arr[:, :,1], arr[:, :,0]) + np.radians(90)
    val = np.rad2deg(ang % consts.PI2)
    val_int = np.around(val).astype(int)

    # Distance for every point
    dist = np.sqrt(arr[:, :, 0] ** 2 + arr[:, :, 1] ** 2)
    min_dist = np.min(dist, axis=-1)

    # Checking if the angles are on the 360,0 split
    split_mask = (np.max(val, axis=1)-np.min(val, axis=1)) > 180

    v_map = np.zeros([360, len(diff)], dtype=np.float)
    shuffle_v_map = np.roll(np.arange(360), 180)
    v_map[:] = np.inf

    val_int[val_int < 180 * split_mask[..., None]] += 360
    val_int[split_mask] -= 180

    v_min = np.min(val_int, axis=-1)
    v_max = np.max(val_int, axis=-1)

    for i, m_dist in enumerate(min_dist):
        if split_mask[i]:
            v_map[shuffle_v_map[v_min[i]:v_max[i]]] = m_dist
        else:
            v_map[v_min[i]:v_max[i], i] = m_dist

    # Getting min value over all points
    v_map = np.min(v_map, axis=1)

    return v_map











    # quit()
    #
    #
    # print ("ddddddddddddd", ang)
    #
    # dist = np.sqrt(diff[:, 0] ** 2 + diff[:, 1] ** 2)
    #
    #
    # map = np.zeros([360], dtype=np.float)
    # map[:] = np.nan
    #
    #
    #
    #
    #
    #
    # for idx in range(len(angle_bounds)-1):
    #     angle_min = angle_bounds[idx]
    #     angle_max = angle_bounds[idx+1]
    #
    #     # Getting indexes within range
    #     idxs = np.where((val >= angle_min) * (val < angle_max))[0]
    #     if idxs.shape[0]:
    #         moves[idx] = np.min(dist[idxs])
    #     else:
    #         moves[idx] = default_value
    #
    # return moves



def moves2RectangleEdge(point, leftTop, rightBottom, moves=None):
    """ Returns the number of moves to the top, right, bottom, left edge"""
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

def arrShapeMatch(arr, shape):
    """ Checks the the arr.shape matches shape"""
    if not arr.shape == shape:
        raise Exception("Arr shape miss match. Expected {}. Received {}".fomrat(shape, arr.shape))


