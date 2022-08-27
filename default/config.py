from modules import info_utils


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
        'bitrate': ['1pass', '2pass']
    }

    CODEC_PRESET = {
        'libx264': ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'],
        'libx264rgb': ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'],
        'h264_nvenc': ['default', 'slow', 'medium', 'fast', 'hp', 'hq', 'bd', 'll', 'llhq', 'llhp', 'lossless', 'losslesshp', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7'],
        'libx265': ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'],
        'hevc_nvenc': ['default', 'slow', 'medium', 'fast', 'hp', 'hq', 'bd', 'll', 'llhq', 'llhp', 'lossless', 'losslesshp', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7']
    }

    SECTIONS_COMMENT = [['[Optional] Set target framerate for your video'],
                        ['[Optional] Set video quality for your video',
                         'Such as 540, 720, 1080 (For video height)',
                         'If video quality is lower than your setting, program will skip this option'],
                        ['[!Important!][Optional]If you use Hardware Acceleration to speed up encoding, '
                         'you should enable this option', 'Usually you do not need to modify this option',
                         'If you not using nVidia Graphics, you should change this option'],
                        ['Set encoder to convert your video',
                         'Suggest options: ' + "libx264, libx265",
                         'Available options: ' +
                         ', '.join(info_utils.get_encoders()),
                         'Note: Encoders ending in *_nvenc are supported GPU',
                         'Preset is a config item of the encoder. A different encoder has different presets.',
                         'For more information, please check the documentation of the encoder'],
                        ['Set encoder option for task',
                         '>> mode: \'crf\', \'cq\', \'1pass\', \'2pass\'',
                         '>> value: Only available for \'crf\' and \'cq\', adaptive bitrate for video',
                         'You can type 0-51, 0 is lossless, 18 is visually lossless',
                         'Note: 18-28 is recommended, we mostly choose 23.5',
                         '>> bitrate: Only available for \'1pass\' and \'2pass\', lock bitrate for video',
                         'You can type a number only or a number which ends with \'k\''],
                        ['Scan video files as below extension name (split as \'|\')'],
                        ['Prefix and suffix for output file'],
                        ['Output video files extension name (follow codec of your choice)',
                         'Use \'none\' to mark path is not specified',
                         '[Important] You must use \'absolute\' or \'relative\' to mark it is a absolute path or yet'
                         'by \'[]\', such as \'[absolute]D:\\Videos\\Anime\'',
                         'Use [source] to mark output directory is same as input'
                         'Tips: relative mode support \'..\\\' and preset variables',
                         'You can insert preset variables such as {var_name}',
                         'Available variables: {src_dir}'],
                        ['[Optional] To save log for progress'],
                        ['[Optional] Some extra settings',
                         '>> del_src: Delete original file when compress completed',
                         '>> threads: Number of threads to use'],
                        ['[Optional] Skip options',
                         '>> min_skip_bitrate: If bitrate of video is lower than this option, will skip it']]

    SECTIONS_CONF_NAME = [['enable', 'value'],
                          ['enable', 'value'],
                          ['enable', 'hwaccel', 'decoder'],
                          ['encoder', 'preset'],
                          ['enable', 'mode', 'value', 'bitrate'],
                          ['input', 'output'],
                          ['prefix', 'suffix'],
                          ['input', 'output'],
                          ['enable', 'name'],
                          ['del_src', 'threads'],
                          ['min_bitrate']]

    SECTIONS_CONF_VALUE = [['False', '60'],
                           ['False', '720'],
                           ['False', 'cuvid', 'h264_cuvid'],
                           ['libx264', 'medium'],
                           ['True', 'crf', '23.5', '2000k'],
                           ['mp4|mov', 'mp4'],
                           ['[compressed]', ''],
                           ['none', '[relative]out'],
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
