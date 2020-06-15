from logging import debug
import subprocess
import os
import numpy as np

FFMPEG_BIN = 'ffmpeg'

class VideoWriter:
    """ Simple ffmpeg video writer """

    DEFAULT_FPS = 24

    def __init__(self, file_path, input_width, input_height, override=True, fps=None, n_channels=0):

        if not file_path == "-":
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
            #'-f', 'image2pipe'
            '-f', 'rawvideo',
            '-s', '{}x{}'.format(input_width, input_height),
            '-pix_fmt', pix_fmt,
            '-r', '{:f}'.format(fps or self.DEFAULT_FPS),
            '-i', '-',
            '-an',
            #'-preset', 'veryslow'
            '-vcodec', 'rawvideo',

            self.file_path,
        ]

        self.proc = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            #stdout=subprocess.PIPE
        )

    @classmethod
    def from_arr(cls, file_path, arr, **kwargs):
        """ create class via arrs """
        n_channels = 0
        if arr.ndim > 2:
            n_channels = arr.shape[-1]
        input_height, input_width = arr.shape[:2]

        return cls(
            file_path,
            input_width,
            input_height,
            n_channels=n_channels,
            **kwargs
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





def join_videos(out_path, *input_videos):
    """ Joints multiple videos """
    command = [FFMPEG_BIN, "-y", "-f", "concat", "-safe", "0", "-i", r"\tmp\dsdas.txt", "-c", "copy"]
    print (" ".join(command))
    # $ ffmpeg -f concat -safe 0 -i mylist.txt -c copy output.mp4

    with open(r"C:\tmp\dsdas.txt", "w") as FILE:
        for input_video in input_videos:
            FILE.write("file {}\n".format(input_video)) #C:\\tmp\\ paths need \\


    command.append(out_path)
    print (command)
    return subprocess.call(command)

if __name__ == "__main__":


    # import subprocess
    #
    # p2 = subprocess.Popen(["echo", "sdsds"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    #
    #
    #
    # #proc.stdin.write("ss")
    #
    # stdout_value = proc.communicate('through stdin to stdout')[0]
    # print ('\tpass through:', repr(stdout_value))
    #
    #
    # quit()
    #
    #
    writer = VideoWriter(r"C:\\tmp\\test.mp4", 10, 10, n_channels=3)
    for i in range(300):
        arr = np.zeros([10, 10, 3], dtype=np.uint8)
        index = np.unravel_index((i), arr.shape)
        arr[index] = 255
        print (writer.write_im(arr))

    writer.close()
    quit()


     #print (writer.write_im(arr))
    # #print (writer.proc.communicate())
    #
    # print (writer.proc.stdout.read(10000))
    from pathlib import Path

    # for path in Path(r"C:\tmp").glob("generation.{:04d}.mp4"):
    #     print (path)
    input_paths = []
    for i in range(1, 10000):
        path = r"C:\\tmp\\generation.{:04d}.mp4".format(i)
        if not os.path.exists(path):
            break
        input_paths.append(path)

    print (input_paths)

    join_videos(r"C:\tmp\generation.mp4", *input_paths)



