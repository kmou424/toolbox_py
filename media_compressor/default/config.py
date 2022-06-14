from bin import info_utils


class VideoConf:
    SECTIONS = ['TARGET_COMPRESS_RATE',
                'TARGET_FRAMERATE',
                'TARGET_QUALITY',
                'TARGET_DECODER',
                'TARGET_ENCODER',
                'TARGET_ENCODER_PRESET',
                'IO_FORMAT',
                'IO_FIX',
                'IO_DIR',
                'LOGGING',
                'EXTRA',
                'SKIP']

    CODEC_PRESET = ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow']

    SECTIONS_COMMENT = [['Set target compress rate for your video', 'compress_arg: \'crf\' or \'qp\'',
                         'You can type 0-51, 0 is lossless, 18 is visually lossless',
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
                         'Note: Encoders ending in *_nvenc are supported GPU',
                         'custom_yuv_pix_fmt: If you want to customize the color space and bit depth of the yuv color'
                         ' encoder, please enable this option',
                         'If you don\'t know what it means, Google it or disable it',
                         '[Warning] Hardware Acceleration is not support 422 color space and 10bit of yuv',
                         'yuv_colorspace: 420 422 444',
                         'yuv_bit_depth: 8 10'],
                        ['Set ffmpeg preset for codec (control progress speed and quality of output video)',
                         'Available options: ' + ', '.join(CODEC_PRESET)],
                        ['Scan video files as below extension name (split as \'|\')'],
                        ['Prefix and suffix for output file'],
                        ['Output video files extension name (follow codec of your choice)',
                         'Use \'none\' to mark path is not specified',
                         '[Important] You must use \'absolute\' or \'relative\' to mark it is a absolute path or yet'
                         'by \'[]\', such as \'[absolute]D:\\Videos\\Anime\'',
                         'Use [source] to mark output directory is same as input'],
                        ['[Optional] To save log for progress'],
                        ['[Optional] Some extra settings', 'del_src: Delete original file when compress completed'],
                        ['[Optional] Skip options',
                         'min_skip_bitrate: If bitrate of video is lower than this option, will skip it']]

    SECTIONS_CONF_NAME = [['compress_arg', 'value'],
                          ['enable', 'value'],
                          ['enable', 'value'],
                          ['enable', 'hwaccel', 'decoder'],
                          ['encoder', 'custom_yuv_pix_fmt', 'yuv_colorspace', 'yuv_bit_depth'],
                          ['enable', 'value'],
                          ['input', 'output'],
                          ['prefix', 'suffix'],
                          ['input', 'output'],
                          ['enable', 'name'],
                          ['del_src'],
                          ['min_bitrate']]

    SECTIONS_CONF_VALUE = [['crf', '23.5'],
                           ['False', '60'],
                           ['False', '720'],
                           ['False', 'cuvid', 'h264_cuvid'],
                           ['libx264', 'False', '420', '8'],
                           ['True', 'medium'],
                           ['mp4|mov', 'mp4'],
                           ['[compressed]', ''],
                           ['none', '[relative]out'],
                           ['False', 'log_video.txt'],
                           ['False'],
                           ['0']]


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
                         '[Important] You must use \'absolute\' or \'relative\' to mark it is a absolute path or yet'
                         'by \'[]\', such as \'[absolute]D:\\Videos\\Anime\'',
                         'Use [source] to mark output directory is same as input'],
                        ['[Optional] To save log for progress']]

    SECTIONS_CONF_NAME = [['value'],
                          ['input', 'output'],
                          ['input', 'output'],
                          ['enable', 'name']]

    SECTIONS_CONF_VALUE = [['2'],
                           ['jpg|png', 'jpg'],
                           ['none', '[relative]out'],
                           ['True', 'log_image.txt']]
