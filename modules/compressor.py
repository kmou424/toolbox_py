from multiprocessing import cpu_count
import os

import configparser
import ffpb

from modules import charparser, info_utils
from pathlib import Path


class __CommonOutput:
    OUTPUT_DIR = ''
    OUTPUT_FORMAT = ''
    FILENAME_EXT = ''
    FILENAME = ''

    def __init__(self, config_parser: configparser.ConfigParser, filepath: str):
        self.OUTPUT_DIR = charparser.parse_path(
            config_parser.get('IO_DIR', 'output'), filepath)
        if not Path(self.OUTPUT_DIR).exists():
            os.makedirs(self.OUTPUT_DIR)
        self.OUTPUT_FORMAT = config_parser.get('IO_FORMAT', 'output')
        for i in range(len(filepath) - 1, 0, -1):
            if filepath[i] == charparser.get_path_delimiter():
                self.FILENAME_EXT = filepath[-(len(filepath) - i - 1):]
                break
        for i in range(len(self.FILENAME_EXT) - 1, 0, -1):
            if self.FILENAME_EXT[i] == '.':
                self.FILENAME = self.FILENAME_EXT[0:i]
                break


ARGS = dict()


def add_arg(option: str, value: str):
    ARGS[option] = value


def has_arg(option: str):
    return option in ARGS


def compress(config_parser: configparser.ConfigParser, filepath: str, task_cnt: int, compress_target: str):
    if compress_target == 'video':
        compress_video(config_parser, filepath, task_cnt)
    elif compress_target == 'image':
        compress_image(config_parser, filepath, task_cnt)


def compress_video(config_parser: configparser.ConfigParser, filepath: str, task_cnt: int):
    _VIDEO_INFO = info_utils.Video(filepath)
    _SIZE = _VIDEO_INFO.size
    # Decoder
    _DECODER_ENABLED = config_parser.get('TARGET_DECODER', 'enable')
    _DECODER = 'Default'
    if charparser.Bool(_DECODER_ENABLED):
        _HWACCEL = config_parser.get('TARGET_DECODER', 'hwaccel')
        _DECODER = config_parser.get('TARGET_DECODER', 'decoder')
        add_arg('-hwaccel', _HWACCEL)
        add_arg('-c:v', _DECODER)
    # Input file
    add_arg('-i', filepath)
    # Compress arg
    _COMPRESS_ARG_ENABLED = config_parser.get('TARGET_COMPRESS_RATE', 'enable')
    _COMPRESS_ARG = 'None'
    _COMPRESS_ARG_VALUE = 'None'
    if charparser.Bool(_COMPRESS_ARG_ENABLED):
        _COMPRESS_ARG = config_parser.get(
            'TARGET_COMPRESS_RATE', 'compress_arg')
        _COMPRESS_ARG_VALUE = config_parser.get(
            'TARGET_COMPRESS_RATE', 'value')
        if _COMPRESS_ARG == 'crf':
            add_arg('-crf:v', _COMPRESS_ARG_VALUE)
        if _COMPRESS_ARG == 'cq':
            add_arg('-cq:v', str(int(float(_COMPRESS_ARG_VALUE))))
            add_arg('-qmin', str(int(float(_COMPRESS_ARG_VALUE))))
            add_arg('-qmax', str(int(float(_COMPRESS_ARG_VALUE))))
        if _COMPRESS_ARG != 'cq' and _COMPRESS_ARG != 'crf':
            _COMPRESS_ARG = 'None'
            _COMPRESS_ARG_VALUE = 'None'
    # Framerate
    _SRC_FRAMERATE = _VIDEO_INFO.framerate
    _SRC_FRAMERATE_DISPLAY = "Unknown"
    _RES_FRAMERATE_ENABLED = config_parser.get('TARGET_FRAMERATE', 'enable')
    if _SRC_FRAMERATE is not None:
        _SRC_FRAMERATE_DISPLAY = str(_SRC_FRAMERATE) + 'fps'
    _RES_FRAMERATE_DISPLAY = _SRC_FRAMERATE_DISPLAY
    if _SRC_FRAMERATE is not None and charparser.Bool(_RES_FRAMERATE_ENABLED):
        _RES_FRAMERATE = config_parser.get('TARGET_FRAMERATE', 'value')
        add_arg('-r', _RES_FRAMERATE)
        _RES_FRAMERATE_DISPLAY += ' fps'
    else:
        _RES_FRAMERATE_DISPLAY += '(Unchanged)'

    # Quality
    _QUALITY = config_parser.get('TARGET_QUALITY', 'enable')
    _SRC_RESOLUTION_DISPLAY = "Unknown"
    if _SIZE is not None:
        _SRC_RESOLUTION_DISPLAY = "{width}x{height}".format(
            width=_SIZE[0], height=_SIZE[1])
    _RES_RESOLUTION_DISPLAY = _SRC_RESOLUTION_DISPLAY
    if _SIZE is not None and charparser.Bool(_QUALITY):
        _QUALITY_VALUE = float(config_parser.get('TARGET_QUALITY', 'value'))
        _WIDTH = float(_SIZE[0])
        _HEIGHT = float(_SIZE[1])
        if _HEIGHT > _WIDTH:
            # 竖屏视频
            if _WIDTH > _QUALITY_VALUE:
                _ZOOM_RATIO = _QUALITY_VALUE / _WIDTH
                _HEIGHT = _HEIGHT * _ZOOM_RATIO
                _WIDTH = _QUALITY_VALUE
        else:
            # 横屏视频
            if _HEIGHT > _QUALITY_VALUE:
                _ZOOM_RATIO = _QUALITY_VALUE / _HEIGHT
                _HEIGHT = _QUALITY_VALUE
                _WIDTH = _WIDTH * _ZOOM_RATIO
        add_arg('-vf', 'scale=' +
                str(_WIDTH) + ':' + str(_HEIGHT))
        _RES_RESOLUTION_DISPLAY = "{width}x{height}".format(
            width=int(_WIDTH), height=int(_HEIGHT))

    # Encoder
    _HW_ENABLED = False
    _ENCODER = config_parser.get('TARGET_ENCODER', 'encoder')
    if _ENCODER in info_utils.get_encoders():
        add_arg('-c:v', _ENCODER)
        add_arg('-preset:v', 'slow')
        if _ENCODER.__contains__('nvenc')\
                or _ENCODER.__contains__('qsv')\
                or _ENCODER.__contains__('amf'):
            _HW_ENABLED = True
            add_arg('-preset:v', 'p7')
    else:
        _ENCODER = _ENCODER + '(Invalid)'

    # Extra argument
    # add_arg('-multipass', 'fullres')
    add_arg('-tier:v', 'high')
    if '480' in _RES_RESOLUTION_DISPLAY:
        add_arg('-level:v', '3.1')
    if '720' in _RES_RESOLUTION_DISPLAY:
        add_arg('-level:v', '4.2')
    if '1080' in _RES_RESOLUTION_DISPLAY:
        add_arg('-level:v', '5.2')
    if '2160' in _RES_RESOLUTION_DISPLAY:
        add_arg('-level:v', '6.2')
    add_arg('-rc:v', 'vbr')

    # Output file
    _OUTPUT_INFO = __CommonOutput(config_parser, filepath)
    _PREFIX = config_parser.get('IO_FIX', 'prefix')
    _SUFFIX = config_parser.get('IO_FIX', 'suffix')
    OUT_FILEPATH = "{dir}{delimiter}{prefix}{filename}{suffix}.{format}".format(dir=_OUTPUT_INFO.OUTPUT_DIR,
                                                                                delimiter=charparser.get_path_delimiter(),
                                                                                prefix=_PREFIX,
                                                                                filename=_OUTPUT_INFO.FILENAME,
                                                                                suffix=_SUFFIX,
                                                                                format=_OUTPUT_INFO.OUTPUT_FORMAT)

    # EXTRA
    _DEL_SRC = config_parser.get('EXTRA', 'del_src')
    _THREADS = config_parser.get('EXTRA', 'threads')
    if _THREADS.isdigit() and cpu_count() >= int(_THREADS) >= 1:
        add_arg('-threads', _THREADS)
    else:
        _THREADS += '(Invalid)'

    # SKIP
    _SKIP_MIN_BITRATE = int(config_parser.get('SKIP', 'min_bitrate'))

    _BITRATE_V = _VIDEO_INFO.bitrate
    _BITRATE_DISPLAY = str(_BITRATE_V) + ' kbps'

    if _BITRATE_V is None:
        _BITRATE_DISPLAY = 'Unknown'

    print()
    print("当前工作路径: " + os.getcwd())
    print("第" + str(task_cnt) + "个视频处理任务")
    print("输入文件名: " + _OUTPUT_INFO.FILENAME_EXT)
    print("输出文件名: {prefix}{filename}{suffix}.{format}".format(
        prefix=_PREFIX,
        filename=_OUTPUT_INFO.FILENAME,
        suffix=_SUFFIX,
        format=_OUTPUT_INFO.OUTPUT_FORMAT))
    print("输出位置: " + _OUTPUT_INFO.OUTPUT_DIR)
    print("视频码率: " + _BITRATE_DISPLAY)
    print("视频帧率: {src} -> {res}".format(src=_SRC_FRAMERATE_DISPLAY,
          res=_RES_FRAMERATE_DISPLAY))
    print("压缩方法和压缩率: {arg} {comp_value}".format(
        arg=_COMPRESS_ARG, comp_value=_COMPRESS_ARG_VALUE))
    print(
        "分辨率: {src} -> {res}".format(src=_SRC_RESOLUTION_DISPLAY, res=_RES_RESOLUTION_DISPLAY))
    print("解码器: " + _DECODER)
    print("编码器: {encoder}".format(encoder=_ENCODER))
    print("硬件加速: " + str(_HW_ENABLED))
    print("线程数: " + _THREADS)
    _LOG_FILE_ENABLE = config_parser.get('LOGGING', 'enable')
    _LOG_FILE = ''
    if charparser.Bool(_LOG_FILE_ENABLE):
        _LOG_FILE = open(os.getcwd() + charparser.get_path_delimiter() +
                         config_parser.get('LOGGING', 'name'), 'a', encoding='utf-8')

    if _BITRATE_V is not None and _BITRATE_V < _SKIP_MIN_BITRATE:
        print("此视频比特率过低，跳过压制")
    else:
        print("开始压制视频...")
        if charparser.Bool(_LOG_FILE_ENABLE):
            _LOG_FILE.write("[" + str(task_cnt) + "] " + filepath +
                            "\n    Compress Rate: {arg} {comp_value}".format(arg=_COMPRESS_ARG, comp_value=_COMPRESS_ARG_VALUE) +
                            "\n    Framerate: " + _SRC_FRAMERATE_DISPLAY + " -> " + _RES_FRAMERATE_DISPLAY +
                            "\n    Resolution: {src} -> {res}".format(src=_SRC_RESOLUTION_DISPLAY, res=_RES_RESOLUTION_DISPLAY) +
                            "\n    Decoder: " + _DECODER +
                            "\n    Encoder: {encoder}".format(encoder=_ENCODER) +
                            "\n    Hardware Acceleration: " + str(_HW_ENABLED) + '\n')
        _COMMAND = []
        for key in ARGS:
            _COMMAND.append(key)
            _COMMAND.append(ARGS[key])
        _COMMAND.append(OUT_FILEPATH)
        print('Shell Args: ' + ' '.join(_COMMAND))
        _RET = ffpb.main(_COMMAND, encoding='utf-8')
        if _RET != 0:
            print("压制失败!")
        else:
            if charparser.Bool(_DEL_SRC):
                os.remove(filepath)
    print()


def compress_image(config_parser: configparser.ConfigParser, filepath: str, task_cnt: int):
    _IMAGE_INFO = info_utils.Image(filepath)
    _SIZE = _IMAGE_INFO.size
    # Input file
    add_arg('-i', filepath)
    # Quality
    _QUALITY = config_parser.get('TARGET_QUALITY', 'value')
    add_arg('-q:v', _QUALITY)
    # Output file
    _OUTPUT_INFO = __CommonOutput(config_parser, filepath)
    OUT_FILEPATH = _OUTPUT_INFO.OUTPUT_DIR + charparser.get_path_delimiter() + \
        _OUTPUT_INFO.FILENAME + '.' + _OUTPUT_INFO.OUTPUT_FORMAT

    # Quality
    _QUALITY = config_parser.get('TARGET_RESOLUTION', 'enable')
    _SRC_RESOLUTION_DISPLAY = "Unknown"
    if _SIZE is not None:
        _SRC_RESOLUTION_DISPLAY = "{width}x{height}".format(
            width=_SIZE[0], height=_SIZE[1])
    _RES_RESOLUTION_DISPLAY = _SRC_RESOLUTION_DISPLAY
    if _SIZE is not None and charparser.Bool(_QUALITY):
        _QUALITY_VALUE = float(config_parser.get('TARGET_RESOLUTION', 'value'))
        _WIDTH = float(_SIZE[0])
        _HEIGHT = float(_SIZE[1])
        if _HEIGHT > _WIDTH:
            # 竖图
            if _WIDTH > _QUALITY_VALUE:
                _ZOOM_RATIO = _QUALITY_VALUE / _WIDTH
                _HEIGHT = _HEIGHT * _ZOOM_RATIO
                _WIDTH = _QUALITY_VALUE
        else:
            # 横图
            if _HEIGHT > _QUALITY_VALUE:
                _ZOOM_RATIO = _QUALITY_VALUE / _HEIGHT
                _HEIGHT = _QUALITY_VALUE
                _WIDTH = _WIDTH * _ZOOM_RATIO
        add_arg('-vf', 'scale=' +
                str(_WIDTH) + ':' + str(_HEIGHT))
        _RES_RESOLUTION_DISPLAY = "{width}x{height}".format(
            width=int(_WIDTH), height=int(_HEIGHT))

    # EXTRA
    _DEL_SRC = config_parser.get('EXTRA', 'del_src')

    print()
    print("当前工作路径: " + os.getcwd())
    print("第" + str(task_cnt) + "个图片处理任务")
    print("输入文件名: " + _OUTPUT_INFO.FILENAME_EXT)
    print("输出文件名: " + _OUTPUT_INFO.FILENAME + '.' + _OUTPUT_INFO.OUTPUT_FORMAT)
    print("压缩质量: " + _QUALITY)
    print(
        "分辨率: {src} -> {res}".format(src=_SRC_RESOLUTION_DISPLAY, res=_RES_RESOLUTION_DISPLAY))
    _COMMAND = []
    for key in ARGS:
        _COMMAND.append(key)
        _COMMAND.append(ARGS[key])
    _COMMAND.append(OUT_FILEPATH)
    _RET = ffpb.main(_COMMAND, encoding='utf-8')
    _IMAGE_OUT_INFO = info_utils.Image(_OUTPUT_INFO.OUTPUT_DIR + charparser.get_path_delimiter() +
                                       _OUTPUT_INFO.FILENAME + '.' + _OUTPUT_INFO.OUTPUT_FORMAT)

    _LOG_FILE_ENABLE = config_parser.get('LOGGING', 'enable')
    _LOG_FILE = ''
    if charparser.Bool(_LOG_FILE_ENABLE):
        _LOG_FILE = open(os.getcwd() + charparser.get_path_delimiter() +
                         config_parser.get('LOGGING', 'name'), 'a', encoding='utf-8')
        _LOG_FILE.write("[" + str(task_cnt) + "]" + _OUTPUT_INFO.FILENAME_EXT + ": " +
                        "\n    Input File Path: " + filepath + " (" + _IMAGE_INFO.fileSizeStr + ")" +
                        "\n    Output File Path: " + _OUTPUT_INFO.OUTPUT_DIR + charparser.get_path_delimiter() +
                        _OUTPUT_INFO.FILENAME + '.' + _OUTPUT_INFO.OUTPUT_FORMAT + " (" + _IMAGE_OUT_INFO.fileSizeStr +
                        ")" + '\n')
    if _RET != 0:
        print("压缩失败!")
    else:
        if charparser.Bool(_DEL_SRC):
            os.remove(filepath)
    print()
