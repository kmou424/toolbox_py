import os

import configparser
import ffpb

from modules import charparser, info_utils
from default import config
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
    # Decoder
    _DECODER_ENABLED = config_parser.get('TARGET_DECODER', 'enable')
    _DECODER = 'Default'
    if charparser.Bool(_DECODER_ENABLED):
        _HWACCEL = config_parser.get('TARGET_DECODER', 'hwaccel')
        _DECODER = config_parser.get('TARGET_DECODER', 'decoder')
        addCommand(_COMMAND, '-hwaccel', _HWACCEL)
        addCommand(_COMMAND, '-c:v', _DECODER)
    # Input file
    addCommand(_COMMAND, '-i', filepath)
    # Compress arg
    _COMPRESS_ARG = config_parser.get('TARGET_COMPRESS_RATE', 'compress_arg')
    _COMPRESS_ARG_VALUE = config_parser.get('TARGET_COMPRESS_RATE', 'value')
    if _COMPRESS_ARG == 'crf':
        addCommand(_COMMAND, '-crf', _COMPRESS_ARG_VALUE)
    if _COMPRESS_ARG == 'qp':
        addCommand(_COMMAND, '-qp', str(int(float(_COMPRESS_ARG_VALUE))))
    if _COMPRESS_ARG != 'qp' and _COMPRESS_ARG != 'crf':
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
        addCommand(_COMMAND, '-r', _RES_FRAMERATE)
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
            # ????????????
            if _WIDTH > _QUALITY_VALUE:
                _ZOOM_RATIO = _QUALITY_VALUE / _WIDTH
                _HEIGHT = _HEIGHT * _ZOOM_RATIO
                _WIDTH = _QUALITY_VALUE
        else:
            # ????????????
            if _HEIGHT > _QUALITY_VALUE:
                _ZOOM_RATIO = _QUALITY_VALUE / _HEIGHT
                _HEIGHT = _QUALITY_VALUE
                _WIDTH = _WIDTH * _ZOOM_RATIO
        addCommand(_COMMAND, '-vf', 'scale=' +
                   str(_WIDTH) + ':' + str(_HEIGHT))
        _RES_RESOLUTION_DISPLAY = "{width}x{height}".format(
            width=int(_WIDTH), height=int(_HEIGHT))

    # Encoder
    _HW_ENABLED = False
    _ENCODER = config_parser.get('TARGET_ENCODER', 'encoder')
    _CUSTOM_YUV_PIX_FMT = config_parser.get(
        'TARGET_ENCODER', 'custom_yuv_pix_fmt')
    _BIT_DEPTH = config_parser.get('TARGET_ENCODER', 'yuv_bit_depth')
    if _BIT_DEPTH == '10':
        _BIT_DEPTH = '10le'
    else:
        _BIT_DEPTH = ''
    _PIX_FMT = "yuv{colorSpace}p{bitDepth}"\
        .format(colorSpace=config_parser.get('TARGET_ENCODER', 'yuv_colorspace'),
                bitDepth=_BIT_DEPTH)
    if _ENCODER in info_utils.get_encoders():
        addCommand(_COMMAND, '-c:v', _ENCODER)
        if charparser.Bool(_CUSTOM_YUV_PIX_FMT):
            addCommand(_COMMAND, '-pix_fmt', _PIX_FMT)
        else:
            _PIX_FMT = ''
        if _ENCODER.__contains__('nvenc')\
                or _ENCODER.__contains__('qsv')\
                or _ENCODER.__contains__('amf'):
            _HW_ENABLED = True
            if _COMPRESS_ARG == 'crf':
                addCommand(_COMMAND, '-tier', 'high')
                addCommand(_COMMAND, '-rc', 'vbr_hq')
                addCommand(_COMMAND, '-spatial_aq', '1')
    else:
        _ENCODER = _ENCODER + '(??????)'

    # Encoder preset
    _CODEC_PRESET = config_parser.get('TARGET_ENCODER_PRESET', 'enable')
    if charparser.Bool(_CODEC_PRESET):
        _CODEC_PRESET = config_parser.get('TARGET_ENCODER_PRESET', 'value')
        if _CODEC_PRESET in config.VideoConf.CODEC_PRESET:
            addCommand(_COMMAND, '-preset', _CODEC_PRESET)
        else:
            _CODEC_PRESET = _CODEC_PRESET + '(??????)'
    else:
        _CODEC_PRESET = 'none'

    # Output file
    _OUTPUT_INFO = __CommonOutput(config_parser, filepath)
    _PREFIX = config_parser.get('IO_FIX', 'prefix')
    _SUFFIX = config_parser.get('IO_FIX', 'suffix')
    _COMMAND.append("{dir}{delimiter}{prefix}{filename}{suffix}.{format}"
                    .format(dir=_OUTPUT_INFO.OUTPUT_DIR,
                            delimiter=charparser.get_path_delimiter(),
                            prefix=_PREFIX,
                            filename=_OUTPUT_INFO.FILENAME,
                            suffix=_SUFFIX,
                            format=_OUTPUT_INFO.OUTPUT_FORMAT))

    # EXTRA
    _DEL_SRC = config_parser.get('EXTRA', 'del_src')

    # SKIP
    _SKIP_MIN_BITRATE = int(config_parser.get('SKIP', 'min_bitrate'))

    _BITRATE_V = _VIDEO_INFO.bitrate
    _BITRATE_DISPLAY = str(_BITRATE_V) + ' kbps'

    if _BITRATE_V is None:
        _BITRATE_DISPLAY = 'Unknown'

    print()
    print("??????????????????: " + os.getcwd())
    print("???" + str(task_cnt) + "?????????????????????")
    print("???????????????: " + _OUTPUT_INFO.FILENAME_EXT)
    print("???????????????: {prefix}{filename}{suffix}.{format}".format(
        prefix=_PREFIX,
        filename=_OUTPUT_INFO.FILENAME,
        suffix=_SUFFIX,
        format=_OUTPUT_INFO.OUTPUT_FORMAT))
    print("????????????: " + _OUTPUT_INFO.OUTPUT_DIR)
    print("????????????: " + _BITRATE_DISPLAY)
    print("????????????: {src} -> {res}".format(src=_SRC_FRAMERATE_DISPLAY,
          res=_RES_FRAMERATE_DISPLAY))
    print("????????????????????????: {arg} {comp_value}".format(
        arg=_COMPRESS_ARG, comp_value=_COMPRESS_ARG_VALUE))
    print(
        "?????????: {src} -> {res}".format(src=_SRC_RESOLUTION_DISPLAY, res=_RES_RESOLUTION_DISPLAY))
    print("?????????: " + _DECODER)
    print("?????????: {encoder} {pix_fmt}".format(
        encoder=_ENCODER, pix_fmt=_PIX_FMT))
    print("???????????????: " + _CODEC_PRESET)
    print("????????????: " + str(_HW_ENABLED))
    _LOG_FILE_ENABLE = config_parser.get('LOGGING', 'enable')
    _LOG_FILE = ''
    if charparser.Bool(_LOG_FILE_ENABLE):
        _LOG_FILE = open(os.getcwd() + charparser.get_path_delimiter() +
                         config_parser.get('LOGGING', 'name'), 'a', encoding='utf-8')

    if _BITRATE_V is not None and _BITRATE_V < _SKIP_MIN_BITRATE:
        print("???????????????????????????????????????")
    else:
        print("??????????????????...")
        if charparser.Bool(_LOG_FILE_ENABLE):
            _LOG_FILE.write("[" + str(task_cnt) + "] " + filepath +
                            "\n    Compress Rate: {arg} {comp_value}".format(arg=_COMPRESS_ARG, comp_value=_COMPRESS_ARG_VALUE) +
                            "\n    Framerate: " + _SRC_FRAMERATE_DISPLAY + " -> " + _RES_FRAMERATE_DISPLAY +
                            "\n    Resolution: {src} -> {res}".format(src=_SRC_RESOLUTION_DISPLAY, res=_RES_RESOLUTION_DISPLAY) +
                            "\n    Decoder: " + _DECODER +
                            "\n    Encoder: {encoder} {pix_fmt}".format(encoder=_ENCODER, pix_fmt=_PIX_FMT) +
                            "\n    Encoder Preset: " + _CODEC_PRESET +
                            "\n    Hardware Acceleration: " + str(_HW_ENABLED) + '\n')
        _RET = ffpb.main(_COMMAND, encoding='utf-8')
        if _RET != 0:
            print("????????????!")
        else:
            if charparser.Bool(_DEL_SRC):
                os.remove(filepath)
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

    # EXTRA
    _DEL_SRC = config_parser.get('EXTRA', 'del_src')

    print()
    print("??????????????????: " + os.getcwd())
    print("???" + str(task_cnt) + "?????????????????????")
    print("???????????????: " + _OUTPUT_INFO.FILENAME_EXT)
    print("???????????????: " + _OUTPUT_INFO.FILENAME + '.' + _OUTPUT_INFO.OUTPUT_FORMAT)
    print("????????????: " + _QUALITY)
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
        print("????????????!")
    else:
        if charparser.Bool(_DEL_SRC):
            os.remove(filepath)
    print()
