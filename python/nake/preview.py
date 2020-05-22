from logging import debug
import subprocess
import os
import numpy as np

FFMPEG_BIN = 'ffmpeg'

class VideoWriter:
    """ Simple ffmpeg video writer """

    DEFAULT_FPS = 12

    def __init__(self, file_path, input_width, input_height, override=True, fps=None, n_channels=0):
        if not override:
            if os.path.exists(file_path):
                raise Exception("File exists {}".format(file_path))
        dir_name = os.path.dirname(file_path)
        if not os.path.exists(dir_name):
            raise Exception("Dir doesn't exist {}".format(file_path))

        if n_channels == 0:
            pix_fmt = "gray"
        elif n_channels == 3:
            pix_fmt = "rgb24"
        else:
            raise Exception("n_channels {} not supported".format(n_channels))

        self.file_path = file_path
        self.input_width = input_width
        self.input_height = input_height

        self.command = [FFMPEG_BIN,
            '-y',

            '-f', 'rawvideo',
            '-s', '{}x{}'.format(input_width, input_height),
            '-pix_fmt', pix_fmt,
            '-r', '{:f}'.format(fps or self.DEFAULT_FPS),
            '-i', '-',
            '-an',
            '-vcodec', 'h264',
            self.file_path,
        ]

        self.proc = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE
        )


    def write_im(self, im):
        """ write image """
        try:
            return self.proc.stdin.write(im.tobytes())
        except IOError as err:
            _, ffmpeg_error = self.proc.communicate()
            ffmpeg_error = ffmpeg_error.decode()
            raise Exception(ffmpeg_error)

    def close(self):
        """ Closing subprocess"""
        if self.proc:
            self.proc.stdin.close()
            if self.proc.stderr is not None:
                self.proc.stderr.close()
            self.proc.wait()
            self.proc = None
            print ("closing")
