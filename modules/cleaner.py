import os


PASS_MODE_MBTREE_FILES = ['ffmpeg2pass-0.log.mbtree', 'ffmpeg2pass-0.log.mbtree.temp']

PASS_MODE_LOG_FILES = ['ffmpeg2pass-0.log', 'ffmpeg2pass-0.log.temp']

def clean_relative_files(files: list):
    for t in files:
        tmp_path = os.path.join(os.getcwd(), t)
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def create_relative_files(files: list):
    for t in files:
        tmp_path = os.path.join(os.getcwd(), t)
        if not os.path.exists(tmp_path):
            open(tmp_path, 'w', encoding='utf-8').close()