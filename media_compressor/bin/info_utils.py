import os

import ffmpeg.stream


def get_encoders():
    res = os.popen("ffpb -codecs")
    encoders = []
    for line in res.readlines():
        if 'encoders' in line:
            encoders.extend(line[line.rfind('encoders:') + 10:len(line) - 3].split(' '))
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
        stream = get_video_stream_info(filepath)
        self.size = [str(stream['width']), str(stream['height'])]


class Video(Info):
    bitrate = ''
    framerate = ''

    def __init__(self, filepath):
        super().__init__(filepath)
        self.__get_bitrate(filepath)
        self.__get_framerate(filepath)

    def __get_bitrate(self, filepath):
        stream = get_video_stream_info(filepath)
        self.bitrate = float(stream['bit_rate']) / 1000

    def __get_framerate(self, filepath):
        stream = get_video_stream_info(filepath)
        self.framerate = str(stream['r_frame_rate'])


class Image(Info):
    def __init__(self, filepath):
        super().__init__(filepath)
