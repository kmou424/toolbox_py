from language.locale_base import Language, get_default_language
from modules import info_utils


lang = Language(get_default_language(), 'en_US')


class VideoConf:
    SECTIONS = ['TARGET_FRAMERATE',
                'TARGET_QUALITY',
                'TARGET_DECODER',
                'TARGET_ENCODER',
                'TARGET_ENCODER_OPTION',
                'IO_FORMAT',
                'IO_FIX',
                'IO_DIR',
                'LOGGING',
                'EXTRA',
                'SKIP']

    ENCODER_MODE = {
        'value': ['crf', 'cq'],
        'bitrate': ['1pass', '2pass', 'bitrateonly']
    }

    PASS_MODE_TEMP_FILES = ['ffmpeg2pass-0.log.mbtree', 'ffmpeg2pass-0.log',
                            'ffmpeg2pass-0.log.mbtree.temp', 'ffmpeg2pass-0.log.temp']

    ENCODER_RATE_CONTROL = ['vbr', 'vbr_hq', 'cbr']

    CODEC_PRESET = {
        'libx264': ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'],
        'libx264rgb': ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'],
        'h264_nvenc': ['default', 'slow', 'medium', 'fast', 'hp', 'hq', 'bd', 'll', 'llhq', 'llhp', 'lossless', 'losslesshp', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7'],
        'libx265': ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'],
        'hevc_nvenc': ['default', 'slow', 'medium', 'fast', 'hp', 'hq', 'bd', 'll', 'llhq', 'llhp', 'lossless', 'losslesshp', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7']
    }

    SECTIONS_COMMENT = [
        [
            lang.get_string("CONF_VIDEO_FRAMERATE_1")
        ],
        [
            lang.get_string("CONF_VIDEO_QUALITY_1"),
            lang.get_string("CONF_VIDEO_QUALITY_2"),
            lang.get_string("CONF_VIDEO_QUALITY_3")
        ],
        [
            lang.get_string("CONF_VIDEO_DECODER_1"),
            lang.get_string("CONF_VIDEO_DECODER_2"),
            lang.get_string("CONF_VIDEO_DECODER_3")
        ],
        [
            lang.get_string("CONF_VIDEO_ENCODER_1"),
            lang.get_string("CONF_VIDEO_ENCODER_2"),
            lang.get_string("CONF_VIDEO_ENCODER_3") +
            ', '.join(info_utils.get_encoders()),
            lang.get_string("CONF_VIDEO_ENCODER_4"),
            lang.get_string("CONF_VIDEO_ENCODER_5"),
            lang.get_string("CONF_VIDEO_ENCODER_6")
        ],
        [
            lang.get_string("CONF_VIDEO_ENCODER_OPTION_1"),
            lang.get_string("CONF_VIDEO_ENCODER_OPTION_2"),
            lang.get_string("CONF_VIDEO_ENCODER_OPTION_3"),
            lang.get_string("CONF_VIDEO_ENCODER_OPTION_4"),
            lang.get_string("CONF_VIDEO_ENCODER_OPTION_5"),
            lang.get_string("CONF_VIDEO_ENCODER_OPTION_6"),
            lang.get_string("CONF_VIDEO_ENCODER_OPTION_7"),
            lang.get_string("CONF_VIDEO_ENCODER_OPTION_8"),
            lang.get_string("CONF_VIDEO_ENCODER_OPTION_9"),
            lang.get_string("CONF_VIDEO_ENCODER_OPTION_10")
        ],
        [
            lang.get_string("CONF_VIDEO_IO_FORMAT_1"),
            lang.get_string("CONF_VIDEO_IO_FORMAT_2")
        ],
        [
            lang.get_string("CONF_VIDEO_IO_FIX_1")
        ],
        [
            lang.get_string("CONF_VIDEO_IO_DIR_1"),
            lang.get_string("CONF_VIDEO_IO_DIR_2"),
            lang.get_string("CONF_VIDEO_IO_DIR_3"),
            lang.get_string("CONF_VIDEO_IO_DIR_4"),
            lang.get_string("CONF_VIDEO_IO_DIR_5"),
            lang.get_string("CONF_VIDEO_IO_DIR_6"),
            lang.get_string("CONF_VIDEO_IO_DIR_7"),
            lang.get_string("CONF_VIDEO_IO_DIR_8")
        ],
        [
            lang.get_string("CONF_VIDEO_LOGGING_1")
        ],
        [
            lang.get_string("CONF_VIDEO_EXTRA_1"),
            lang.get_string("CONF_VIDEO_EXTRA_2"),
            lang.get_string("CONF_VIDEO_EXTRA_3")
        ],
        [
            lang.get_string("CONF_VIDEO_SKIP_1"),
            lang.get_string("CONF_VIDEO_SKIP_2")
        ]
    ]

    SECTIONS_CONF_NAME = [['enable', 'value'],
                          ['enable', 'value'],
                          ['enable', 'hwaccel', 'decoder'],
                          ['encoder', 'preset'],
                          ['enable', 'mode', 'value', 'bitrate', 'rc'],
                          ['input', 'output'],
                          ['prefix', 'suffix'],
                          ['input', 'ignore_input', 'output'],
                          ['enable', 'name'],
                          ['del_src', 'threads'],
                          ['min_bitrate']]

    SECTIONS_CONF_VALUE = [['False', '60'],
                           ['False', '720'],
                           ['False', 'cuvid', 'h264_cuvid'],
                           ['libx264', 'medium'],
                           ['True', 'crf', '23.5', '2000k', 'vbr'],
                           ['mp4|mov', 'mp4'],
                           ['[compressed]', ''],
                           ['none', '[relative]in|[relative]out', '[relative]out'],
                           ['False', 'log_video.txt'],
                           ['False', '1'],
                           ['0']]


class ImageConf:
    SECTIONS = ['TARGET_QUALITY',
                'TARGET_RESOLUTION',
                'IO_FORMAT',
                'IO_DIR',
                'LOGGING',
                'EXTRA']

    SECTIONS_COMMENT = [['Set target quality to compress image (1 - 50)',
                         'notes: A larger number corresponds to a lower quality.'],
                        ['Limit resolution for your image'],
                        ['Scan image files as below extension name (split as \'|\')'],
                        ['Output image files extension name (follow codec of your choice)',
                         'Use \'none\' to mark path is not specified',
                         '[Important] You must use \'absolute\' or \'relative\' to mark it is a absolute path or yet'
                         'by \'[]\', such as \'[absolute]D:\\Videos\\Anime\'',
                         'Use [source] to mark output directory is same as input',
                         'Tips: relative mode support \'..\\\' and preset variables',
                         'You can insert preset variables such as {var_name}',
                         'Available variables: {src_dir}'],
                        ['[Optional] To save log for progress'],
                        ['[Optional] Some extra settings', 'del_src: Delete original file when compress completed']]

    SECTIONS_CONF_NAME = [['value'],
                          ['enable', 'value'],
                          ['input', 'output'],
                          ['input', 'output'],
                          ['enable', 'name'],
                          ['del_src']]

    SECTIONS_CONF_VALUE = [['2'],
                           ['False', '1080'],
                           ['jpg|png', 'jpg'],
                           ['none', '[relative]out'],
                           ['True', 'log_image.txt'],
                           ['False']]
