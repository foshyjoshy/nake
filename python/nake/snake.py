import numpy as np
import consts





class BodySegment:

    def __init__(self):
        pass






class Snake():


    def __init__(self,  headIdx, length, direction, positions):

        # Check positions shape, dtpye


        self.headIdx = headIdx
        self.length = length
        self.positions = positions
        self.direction = direction


    @classmethod
    def initializeAtPosition(cls, position, direction=consts.STR_DOWN, length=6):
        """ Starts from (x,y) moving in direction with length"""

        positions = np.ones([max(length*2, 1024), 2], dtype=np.uint16)*-1
        positions[-length:] = position
        headIdx = positions.shape[0]-length

        if direction.lower() == consts.STR_UP:
            positions[headIdx+1:, 1]+=np.arange(1, length, dtype=np.uint16)
        elif direction.lower() == consts.STR_DOWN:
            positions[headIdx+1:, 1]-=np.arange(1, length, dtype=np.uint16)
        elif direction.lower() == consts.STR_LEFT:
            positions[headIdx+1:, 0] += np.arange(1, length, dtype=np.uint16)
        elif direction.lower() == consts.STR_RIGHT:
            positions[headIdx+1:, 0] -= np.arange(1, length, dtype=np.uint16)
        else:
            raise Exception("{} it not a valid direction... using one of {}".format(direction, consts.DISTANCES_STR))

        return headIdx, length, direction, position


    def moveLeft(self):










        print (positions[1018:])
        #quit()



        #return cls(positions, direction, length)




Snake.initializeAtPosition((10,10), direction=consts.STR_UP)














