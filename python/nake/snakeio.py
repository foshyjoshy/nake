import numpy as np
import zipfile
from io import BytesIO
from enum import Enum
import os
from contextlib import contextmanager


class DirectoryNames(Enum):
    BRAIN = "brains"
    SNAKE = "snakes"
    FOODS = "foods"
    STATS = "stats"

    @property
    def dir(self):
        return self.join("")

    def join(self, name):
        return os.path.join(self.value, name)


class Writer:
    """ Writes object for needed data"""

    def __init__(self, file_path, compression=zipfile.ZIP_DEFLATED):
        self.zip = zipfile.ZipFile(file_path, 'w', compression)
        # Adding default directory names
        #for directory in DirectoryNames:
        #    self.zip.writestr(zipfile.ZipInfo(directory.dir), "")

    @property
    def filename(self):
        return self.zip.filename

    def close(self):
        self.zip.close()

    def write_brain(self, brain, name=None):
        """ Writes brain to compresses zip"""
        if name is None:
            name = "{}.npz".format(brain.name)
        elif name.endswith(".npz"):
            name += ".npz"
        if not os.path.basename(name) == name:
            raise Exception("Name contains a directory {}".format(name))
        filename = DirectoryNames.BRAIN.join(name)

        F = BytesIO()
        brain.save(F, compressed=False)
        self.zip.writestr(filename, F.getbuffer())
        return filename

    def write_food(self, food, name):
        """ Writes food to compresses zip"""
        if name.endswith(".npz"):
            name += ".npz"
        if not os.path.basename(name) == name:
            raise Exception("Name contains a directory {}".format(name))
        filename = DirectoryNames.FOODS.join(name)

        F = BytesIO()
        food.save(F, compressed=False)
        self.zip.writestr(filename, F.getbuffer())
        return filename

    def write_snake(self, snake, name=None):
        """ Writes snake to compresses zip"""
        if name is None:
            if not len(snake.name):
                raise Exception("Snake name is none {}".format(snake))
            name = "{}.npz".format(snake.name)
        elif name.endswith(".npz"):
            name += ".npz"
        if not os.path.basename(name) == name:
            raise Exception("Name contains a directory {}".format(name))
        filename = DirectoryNames.SNAKE.join(name)

        F = BytesIO()
        snake.save(F, compressed=False)
        self.zip.writestr(filename, F.getbuffer())
        return filename

    def write_stats(self, stats, name):
        """ Writes stats to compresses zip"""
        filename = DirectoryNames.STATS.join(name)
        return self.write_numpy_arr(stats.stats, filename) #TODO smarter

    def write_numpy_arr(self, arr, filename):
        """ writes numpy arr to zip"""
        if filename.endswith(".npy"):
            filename += ".npy"
        F = BytesIO()
        np.save(F, arr)
        self.zip.writestr(filename, F.getbuffer())
        return filename



class Reader:
    """ Writes object for needed data"""

    def __init__(self, file_path):
        self.zip = zipfile.ZipFile(file_path, 'r')
        self._brains_info = None
        self._snakes_info = None
        self._foods_info = None
        self._stats_info = None

    def _generate_info_lists(self):
        """ """
        self._brains_info = []
        self._snakes_info = []
        self._foods_info = []
        self._stats_info = []

        map_dirname2list = {
            DirectoryNames.BRAIN.value: self._brains_info,
            DirectoryNames.SNAKE.value: self._snakes_info,
            DirectoryNames.FOODS.value: self._foods_info,
            DirectoryNames.STATS.value: self._stats_info,
        }

        for info in self.zip.infolist():
            if info.is_dir():
                continue
            _list = map_dirname2list.get(os.path.dirname(info.filename), None)
            if _list is not None:
                _list.append(info)

    @property
    def nr_brains(self):
        return len(self.brains_info)

    @property
    def nr_foods(self):
        return len(self.foods_info)

    @property
    def nr_snakes(self):
        return len(self.snake_info)

    @property
    def brains_info(self):
        """ Returns a list of the brain ZipInfo"""
        if self._brains_info is None:
            self._generate_info_lists()
        return self._brains_info

    @property
    def foods_info(self):
        """ Returns a list of the foods ZipInfo"""
        if self._foods_info is None:
            self._generate_info_lists()
        return self._foods_info

    @property
    def snake_info(self):
        """ Returns a list of the snake ZipInfo"""
        if self._snakes_info is None:
            self._generate_info_lists()
        return self._snakes_info

    @property
    def stats_info(self):
        """ Returns a list of the stats ZipInfo"""
        if self._stats_info is None:
            self._generate_info_lists()
        return self._stats_info

    def read_bytesIO(self, file_path):
        """ Reads data into BytesIO"""
        return BytesIO(self.zip.read(file_path))

    def read_numpy(self, file_path, allow_pickle=True):
        """ Reads numpy file from zip"""
        return np.load(self.read_bytesIO(file_path), allow_pickle=allow_pickle)


