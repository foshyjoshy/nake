from enum import Enum
import numpy as np


class RunStats(str, Enum):
    """ Run stat enum"""

    TERM = ("term", np.int32)
    LENGTH = ("length", np.int32)
    MOVES_REMAINING = ("moves_remaining", np.int32)
    MOVES_MADE = ("moves_made", np.int32)
    MOVES_PER_FOOD = ("moves_per_food", np.float)
    DIRECTION = ("direction", np.int32)

    def __new__(cls, value, dtype):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.dtype = dtype
        return obj


class RunStatsStash:
    """ Stashing stats while running snake"""

    DEFAULT_VALUE = -1

    def __init__(self, stash_size, key_instance=None, default_value=None):
        self.default_value = default_value or self.DEFAULT_VALUE
        self.key_instance = key_instance
        self._keys = [None]*stash_size
        self._stats = self.create_array(stash_size, default_value=default_value)
        self.current_size = 0

    @classmethod
    def create_array(cls, n_values, default_value=None):
        """ Creates an array with this number of values"""
        stats_dtypes = [(stat.value, stat.dtype) for stat in RunStats]
        arr = np.zeros([n_values], dtype=stats_dtypes)
        arr[:] = default_value or cls.DEFAULT_VALUE
        return arr

    @property
    def keys(self):
        return self._keys[:self.current_size]

    @property
    def stats(self):
        return self._stats[:self.current_size]

    def __len__(self):
        return self.current_size

    def get_stats_for_brain(self, brain):
        """ Returns the stats for the given brain"""
        index = self.keys.index(brain.name)
        return self._stats[index]

    def is_full(self):
        """ Returns if the number in the stash match its max size"""
        return self.current_size == len(self._stats)

    def replace(self, index, key, **kwargs):
        """ Replace values at index with **kwargs"""
        if self.key_instance is not None:
            assert isinstance(key, self.key_instance)

        self._keys[index] = key
        self._stats[index] = self.default_value
        for k, value in kwargs.items():
            self._stats[index][k] = value

    def append(self, key, **kwargs):
        """ Appending stats"""
        if self.is_full():
            raise Exception("Stash is full. Unable to add more")
        self.replace(self.current_size, key, **kwargs)
        self.current_size += 1

    def save(self, filepath):
        """ Writes stats to npz """
        return np.save(filepath, stats)



if __name__ == "__main__":

    import os
    import snakeio
    from run_stats import RunStats
    input_paths = []

    total_lengths = []
    lengths = []
    max_lengths = []
    for i in range(1, 10000):
        path = r"C:\\tmp\\generation_2.{:04d}.zip".format(i)
        if not os.path.exists(path):
            break
        input_paths.append(path)


        reader = snakeio.Reader(path)
        length = 0
        max_length  = 0
        for sidc, stats_info in enumerate(reader.stats_info):
            arr = reader.read_numpy(stats_info, True)
            length += np.sum((arr[RunStats.LENGTH]))

        lengths.append( length/(len(arr)*len(reader.stats_info)))

        print (lengths[-1], path, max_length)
        max_lengths.append(max_length)

    import matplotlib.pyplot as plt
    from scipy import interpolate as itp

    plt.subplot(1,2,1)
    plt.plot(lengths)

    x = np.arange(len(lengths))
    mytck, myu = itp.splprep([x, lengths], k=5)
    xnew, ynew = itp.splev(np.linspace(0, 1, 1000), mytck)
    plt.plot(xnew, ynew)


    plt.subplot(1,2,2)
    plt.plot(max_lengths)
    plt.show()


