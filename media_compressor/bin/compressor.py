import os

import configparser
import ffpb

from bin import charparser, info_utils
from default import config
from pathlib import Path


class __CommonOutput:
    OUTPUT_DIR = ''
    OUTPUT_FORMAT = ''
    FILENAME_EXT = ''
    FILENAME = ''

    def __init__(self, config_parser: configparser.ConfigParser, filepath: str):
        self.OUTPUT_DIR = charparser.parse_path(config_parser.get('IO_DIR', 'output'))
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


def addCommand(command: list, option: str, value: str):
    command.append(option)
    command.append(value)


def compress(config_parser: configparser.ConfigParser, filepath: str, task_cnt: int, compress_target: str):
    if compress_target == 'video':
        compress_video(config_parser, filepath, task_cnt)
    elif compress_target == 'image':
        compress_image(config_parser, filepath, task_cnt)


def compress_video(config_parser: configparser.ConfigParser, filepath: str, task_cnt: int):
    _VIDEO_INFO = info_utils.Video(filepath)
    _SIZE = _VIDEO_INFO.size
    _COMMAND = []
    # Input file
    addCommand(_COMMAND, '-i', filepath)
    # Crf
    _CRF = config_parser.get('TARGET_CRF', 'value')
    addCommand(_COMMAND, '-crf', _CRF)
    # Framerate
    _FRAMERATE = config_parser.get('TARGET_FRAMERATE', 'enable')
    _ORI_FRAMERATE = _VIDEO_INFO.framerate + ' fps'
    if charparser.Bool(_FRAMERATE):
        _FRAMERATE = config_parser.get('TARGET_FRAMERATE', 'value')
        addCommand(_COMMAND, '-r', _FRAMERATE)
        _FRAMERATE += ' fps'
    else:
        _FRAMERATE = _ORI_FRAMERATE + '(none)'

    # Quality
    _QUALITY = config_parser.get('TARGET_QUALITY', 'enable')
    _RES_RESOLUTION = "{width}x{height}".format(width=_SIZE[0], height=_SIZE[1])
    if charparser.Bool(_QUALITY):
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
        addCommand(_COMMAND, '-vf', 'scale=' + str(_WIDTH) + ':' + str(_HEIGHT))
        _RES_RESOLUTION = "{width}x{height}".format(width=int(_WIDTH), height=int(_HEIGHT))

    # Encoder
    _CODEC = config_parser.get('TARGET_CODEC', 'value')
    if _CODEC in info_utils.get_encoders():
        addCommand(_COMMAND, '-c:v', _CODEC)
    else:
        _CODEC = _CODEC + '(无效)'

    # Encoder preset
    _CODEC_PRESET = config_parser.get('TARGET_CODEC_PRESET', 'enable')
    if charparser.Bool(_CODEC_PRESET):
        _CODEC_PRESET = config_parser.get('TARGET_CODEC_PRESET', 'value')
        if _CODEC_PRESET in config.VideoConf.CODEC_PRESET:
            addCommand(_COMMAND, '-preset', _CODEC_PRESET)
        else:
            _CODEC_PRESET = _CODEC_PRESET + '(无效)'
    else:
        _CODEC_PRESET = 'none'

    # Output file
    _OUTPUT_INFO = __CommonOutput(config_parser, filepath)
    _COMMAND.append(_OUTPUT_INFO.OUTPUT_DIR + charparser.get_path_delimiter() +
                    _OUTPUT_INFO.FILENAME + '.' + _OUTPUT_INFO.OUTPUT_FORMAT)
    _BITRATE_V = _VIDEO_INFO.bitrate

    print()
    print("当前工作路径: " + os.getcwd())
    print("第" + str(task_cnt) + "个视频处理任务")
    print("输入文件名: " + _OUTPUT_INFO.FILENAME_EXT)
    print("输出文件名: " + _OUTPUT_INFO.FILENAME + '.' + _OUTPUT_INFO.OUTPUT_FORMAT)
    print("输出位置: " + _OUTPUT_INFO.OUTPUT_DIR)
    print("视频码率: " + str(_BITRATE_V) + "k")
    print("视频帧率: " + _FRAMERATE)
    print("目标CRF: " + _CRF)
    print("分辨率: {width}x{height} -> ".format(width=_SIZE[0], height=_SIZE[1]) + _RES_RESOLUTION)
    print("编码器: " + _CODEC)
    print("编码器预设: " + _CODEC_PRESET)
    _LOG_FILE_ENABLE = config_parser.get('LOGGING', 'enable')
    _LOG_FILE = ''
    if charparser.Bool(_LOG_FILE_ENABLE):
        _LOG_FILE = open(_OUTPUT_INFO.OUTPUT_DIR + charparser.get_path_delimiter() +
                         config_parser.get('LOGGING', 'name'), 'a')

    print("开始压缩视频...")
    if charparser.Bool(_LOG_FILE_ENABLE):
        _LOG_FILE.write("[" + str(task_cnt) + "]" +
                        "\n    Input File Path: " + filepath +
                        "\n    CRF:" + _CRF +
                        "\n    Framerate: " + _ORI_FRAMERATE + " -> " + _FRAMERATE +
                        "\n    Resolution: {width}x{height} -> ".format(width=_SIZE[0], height=_SIZE[1]) +
                        _RES_RESOLUTION +
                        "\n    Encoder: " + _CODEC +
                        "\n    Encoder Preset: " + _CODEC_PRESET + "\n")
    ffpb.main(_COMMAND, encoding='utf-8')
    print()


def compress_image(config_parser: configparser.ConfigParser, filepath: str, task_cnt: int):
    _IMAGE_INFO = info_utils.Image(filepath)
    _COMMAND = []
    # Input file
    addCommand(_COMMAND, '-i', filepath)
    # Quality
    _QUALITY = config_parser.get('TARGET_QUALITY', 'value')
    addCommand(_COMMAND, '-q:v', _QUALITY)
    # Output file
    _OUTPUT_INFO = __CommonOutput(config_parser, filepath)
    _COMMAND.append(_OUTPUT_INFO.OUTPUT_DIR + charparser.get_path_delimiter() +
                    _OUTPUT_INFO.FILENAME + '.' + _OUTPUT_INFO.OUTPUT_FORMAT)

    print()
    print("当前工作路径: " + os.getcwd())
    print("第" + str(task_cnt) + "个图片处理任务")
    print("输入文件名: " + _OUTPUT_INFO.FILENAME_EXT)
    print("输出文件名: " + _OUTPUT_INFO.FILENAME + '.' + _OUTPUT_INFO.OUTPUT_FORMAT)
    print("压缩质量: " + _QUALITY)
    ffpb.main(_COMMAND, encoding='utf-8')
    _IMAGE_OUT_INFO = info_utils.Image(_OUTPUT_INFO.OUTPUT_DIR + charparser.get_path_delimiter() +
                                       _OUTPUT_INFO.FILENAME + '.' + _OUTPUT_INFO.OUTPUT_FORMAT)
    _LOG_FILE_ENABLE = config_parser.get('LOGGING', 'enable')
    _LOG_FILE = ''
    if charparser.Bool(_LOG_FILE_ENABLE):
        _LOG_FILE = open(_OUTPUT_INFO.OUTPUT_DIR + charparser.get_path_delimiter() +
                         config_parser.get('LOGGING', 'name'), 'a')
        _LOG_FILE.write("[" + str(task_cnt) + "]" + _OUTPUT_INFO.FILENAME_EXT + ": " +
                        "\n    Input File Path: " + filepath + " (" + _IMAGE_INFO.fileSize + ")" +
                        "\n    Output File Path: " + _OUTPUT_INFO.OUTPUT_DIR + charparser.get_path_delimiter() +
                        _OUTPUT_INFO.FILENAME + '.' + _OUTPUT_INFO.OUTPUT_FORMAT + " (" + _IMAGE_OUT_INFO.fileSize +
                        ")\n")
    print()
