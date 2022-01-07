import os

import ffmpeg.stream


def get_encoders():
    res = os.popen("ffpb -codecs")
    encoders = []
    for line in res.readlines():
        if 'encoders' in line:
            encoders.extend(line[line.rfind('encoders:') + 10:len(line) - 3].split(' '))
    return encoders


class Info:
    fileSize = ''
    size = []

    def __init__(self, filepath):
        self.__get_fileSize(filepath)
        self.__get_size(filepath)

    def __get_fileSize(self, filepath):
        size = os.path.getsize(filepath)
        size = size / float(1024 * 1024)
        self.fileSize = str(round(size, 2)) + "MB"

    def __get_size(self, filepath):
        f = ffmpeg.stream.Stream()
        f.input(filepath)
        self.size = [str(f.video_info().get('streams')[0]['width']),
                     str(f.video_info().get('streams')[0]['height'])]


class Video(Info):
    bitrate = ''
    framerate = ''

    def __init__(self, filepath):
        super().__init__(filepath)
        self.__get_bitrate(filepath)
        self.__get_framerate(filepath)

    def __get_bitrate(self, filepath):
        f = ffmpeg.stream.Stream()
        f.input(filepath)
        self.bitrate = float(f.video_info().get('streams')[0]['bit_rate']) / 1000

    def __get_framerate(self, filepath):
        f = ffmpeg.stream.Stream()
        f.input(filepath)
        self.framerate = str(eval(f.video_info().get('streams')[0]['r_frame_rate']))


class Image(Info):
    def __init__(self, filepath):
        super().__init__(filepath)
