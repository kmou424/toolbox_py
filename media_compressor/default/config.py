from bin import info_utils


class VideoConf:
    SECTIONS = ['TARGET_CRF',
                'TARGET_FRAMERATE',
                'TARGET_QUALITY',
                'TARGET_DECODER',
                'TARGET_ENCODER',
                'TARGET_ENCODER_PRESET',
                'IO_FORMAT',
                'IO_DIR',
                'LOGGING']

    CODEC_PRESET = ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow']

    SECTIONS_COMMENT = [['Set target crf for your video', 'You can type 0-51, 0 is lossless, 18 is visually lossless',
                         'Note: 18-28 is recommended, we mostly choose 23.5'],
                        ['[Optional] Set target framerate for your video'],
                        ['[Optional] Set video quality for your video',
                         'Such as 540, 720, 1080 (For video height)',
                         'If video quality is lower than your setting, program will skip this option'],
                        ['[!Important!][Optional]If you use Hardware Acceleration to speed up encoding, '
                         'you should enable this option', 'Usually you do not need to modify this option',
                         'If you not using nVidia Graphics, you should change this option'],
                        ['Set encoder to convert your video',
                         'Suggest options: ' + "libx264, libx265",
                         'Available options: ' + ', '.join(info_utils.get_encoders()),
                         'Note: Encoders ending in *_nvenc are supported GPU'],
                        ['Set ffmpeg preset for codec (control progress speed and quality of output video)',
                         'Available options: ' + ', '.join(CODEC_PRESET)],
                        ['Scan video files as below extension name (split as \'|\')'],
                        ['Output video files extension name (follow codec of your choice)',
                         'Use \'none\' to mark path is not specified',
                         '[Important] You must use \'absolute\' or \'relative\' to mark it is a absolute path or ye-',
                         't by \'[]\', such as \'[absolute]D:\\Videos\\Anime\''],
                        ['[Optional] To save log for progress']]

    SECTIONS_CONF_NAME = [['value'],
                          ['enable', 'value'],
                          ['enable', 'value'],
                          ['enable', 'hwaccel', 'decoder'],
                          ['encoder'],
                          ['enable', 'value'],
                          ['input', 'output'],
                          ['input', 'output'],
                          ['enable', 'name']]

    SECTIONS_CONF_VALUE = [['23.5'],
                           ['False', '60'],
                           ['False', '720'],
                           ['False', 'cuvid', 'h264_cuvid'],
                           ['libx264'],
                           ['True', 'medium'],
                           ['mp4|mov', 'mp4'],
                           ['none', '[relative]out'],
                           ['True', 'log_video.txt']]


class ImageConf:
    SECTIONS = ['TARGET_QUALITY',
                'IO_FORMAT',
                'IO_DIR',
                'LOGGING']

    SECTIONS_COMMENT = [['Set target quality to compress image (1 - 50)',
                         'notes: A larger number corresponds to a lower quality.'],
                        ['Scan image files as below extension name (split as \'|\')'],
                        ['Output image files extension name (follow codec of your choice)',
                         'Use \'none\' to mark path is not specified',
                         '[Important] You must use \'absolute\' or \'relative\' to mark it is a absolute path or ye-',
                         't by \'[]\', such as \'[absolute]D:\\Images\\Anime\''],
                        ['[Optional] To save log for progress']]

    SECTIONS_CONF_NAME = [['value'],
                          ['input', 'output'],
                          ['input', 'output'],
                          ['enable', 'name']]

    SECTIONS_CONF_VALUE = [['2'],
                           ['jpg|png', 'jpg'],
                           ['none', '[relative]out'],
                           ['True', 'log_image.txt']]
