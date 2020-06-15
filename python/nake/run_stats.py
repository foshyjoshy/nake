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