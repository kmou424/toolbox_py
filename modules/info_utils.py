import os

import ffmpeg.stream


def get_encoders():
    res = os.popen("ffpb -codecs")
    encoders = []
    for line in res.readlines():
        if 'encoders' in line:
            encoders.extend(
                line[line.rfind('encoders:') + 10:len(line) - 3].split(' '))
    return encoders


def get_video_stream_info(filepath):
    f = ffmpeg.stream.Stream()
    f.input(filepath)
    streams = f.video_info().get('streams')
    ret = streams[0]
    for i in streams:
        if i['codec_type'] == 'video':
            ret = i
            break
    return ret


class FileInfo:
    fileSize = 0
    fileSizeStr = ''

    def __init__(self, filepath):
        self.__get_fileSize(filepath)
        self.__get_fileSizeStr()

    def __get_fileSize(self, filepath):
        size = os.path.getsize(filepath)
        self.fileSize = size / float(1024 * 1024)

    def __get_fileSizeStr(self):
        self.fileSizeStr = str(round(self.fileSize, 2)) + "MB"


class Video(FileInfo):
    stream: dict = None
    bitrate: float = None
    framerate: str = None
    size: list = None

    def __init__(self, filepath):
        super().__init__(filepath)
        self.stream = get_video_stream_info(filepath)
        self.__get_bitrate()
        self.__get_framerate()
        self.__get_size()

    def __get_bitrate(self):
        if 'bit_rate' in self.stream.keys():
            self.bitrate = float(self.stream['bit_rate']) / 1000

    def __get_framerate(self):
        if 'r_frame_rate' in self.stream.keys():
            self.framerate = str(self.stream['r_frame_rate'])

    def __get_size(self):
        if 'width' in self.stream.keys() and 'height' in self.stream.keys():
            self.size = [str(self.stream['width']), str(self.stream['height'])]


class Image(FileInfo):
    def __init__(self, filepath):
        super().__init__(filepath)
