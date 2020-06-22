from registry import Registry, RegistryItemBase


class Callbacks(Registry):
    """ A class to store all callbacks"""
    registry = {}



class CallbackBase(RegistryItemBase):
    """" Abstract base class for all callbacks to subclass """

    REGISTRY = Callbacks

    def snake_start(self, snake, brain, board, food_position):
        """ call back before snake starts moving """
        pass

    def snake_move_computed(self, move, snake, brain, board, food_position):
        """ call back before snake moves """
        pass

    def snake_moved(self, snake, brain, board, food_position):
        """ call back after snake is moved """
        pass

    def snake_terminated(self, term, snake, brain, board, food_position):
        """ call back after snake is moved """
        pass


class TestCallback(CallbackBase):
    """ Test callback that prints"""

    def snake_move_computed(self, move, snake, brain, board, food_position):
        """ call back after snake is moved """
        print ("snake_move_computed")
        print (brain.sequential_model.input_arr)

    def snake_moved(self, snake, brain, board, food_position):
        """ call back after snake is moved """
        print ("TestCallback")

    def snake_terminated(self, term, snake, brain, board, food_position):
        """ call back after snake is moved """
        print ("snake_terminated")



from preview import VideoWriter
import numpy as np
import matplotlib

class FlexiDraw(CallbackBase):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.arrs = []
        self.prepend_arrs = []

    def create_array(self):
        """ """
        return np.zeros((self.width, self.height), dtype=np.int64)

    def create_draw_array(self):
        """ """
        return np.zeros((self.width, self.height, 3), dtype=np.uint8)

    def draw_snake(self, snake):
        """ """
        if snake.moves_made >= len(self.arrs):
            self.arrs.append(self.create_array())
        idx = snake.moves_made
        pos = np.clip(snake.arr, (0,0), (self.height-1, self.width-1))
        self.arrs[idx][pos[:,1], pos[:,0]]+=1

    def snake_moved(self, snake, brain, board, food_position):
        self.draw_snake(snake)

    def snake_start(self, snake, brain, board, food_position):
        self.draw_snake(snake)

    def write(self, file_path):

        cmap = matplotlib.cm.get_cmap('inferno')

        writer = VideoWriter.from_arr(file_path, self.create_draw_array())
        for arr in self.prepend_arrs:
            norm = matplotlib.colors.Normalize(vmin=0, vmax=np.max(arr))
            im = (cmap(norm(arr)) * 255).astype(np.uint8)
            writer.write_im(im[:,:,:3][...,::-1])

        total_arr = self.create_array()
        for arr in self.arrs:
            norm = matplotlib.colors.Normalize(vmin=0, vmax=np.max(arr))
            im = (cmap(norm(arr))*255).astype(np.uint8)
            writer.write_im(im[:,:,:3][...,::-1])
            total_arr += arr > 0

        # usage map
        norm = matplotlib.colors.Normalize(vmin=0, vmax=np.max(total_arr))
        im = (cmap(norm(total_arr)) * 255).astype(np.uint8)
        writer.write_im(im[:,:,:3][...,::-1])



        writer.close()