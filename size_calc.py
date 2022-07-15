import os
import sys

from modules import filequery
from modules.info_utils import FileInfo
from modules.io import CustomOut, IOColors


def get_all_files_size(files: list):
    ret = 0
    for _f in files:
        if os.path.isfile(_f):
            ret += FileInfo(_f).fileSize
    return str(round(ret, 2))


def make_output_str(idx: int, param: dict, max_idx_width, max_size_width):
    return "{idx}{size}MB] {name}".format(
        idx=('{:' + str(max_idx_width) +
             '}').format('[' + str(idx).zfill(max_idx_width - 3) + ']'),
        size=('{:' + str(max_size_width) + '}').format('[' + param['size']),
        name=param['name'])


def print_help():
    print("Usage: size_calc.py -s[Sort_Object] -r[Sort_Order]")
    print("\t-s:\t[Optional]Sort object;"
          "\n\t\tValues: \'name\'(file name) or \'size\'(file size);"
          "\n\t\tDefault: \'name\'")
    print("\t-r:\t[Optional]Sort order;"
          "\n\t\tValues: \'upper\' or \'lower\'(reverse from upper);"
          "\n\t\tDefault: \'upper\'")


PWD = os.getcwd()

SORT_OBJ = 'name'
SORT_OBJ_IS_NUMBER = False
SORT_REVERSE = False


for i in sys.argv:
    if i == '-h' or i == '--help':
        print_help()
        exit(0)
    if i.startswith('-s'):
        SORT_OBJ = i.replace('-s', '')
        if SORT_OBJ == 'size':
            SORT_OBJ_IS_NUMBER = True
    if i.startswith('-r'):
        REVERSE = i.replace('-r', '')
        if REVERSE.lower() == 'upper':
            SORT_REVERSE = False
        if REVERSE.lower() == 'lower':
            SORT_REVERSE = True


SURFACE_FILE_LIST = filequery.list_files_and_directories(PWD)

print("Path: " + PWD)

RES = []
DIRS_RES = []
FILE_RES = []

size_max_width = 0
idx_max_width = 0

for f in SURFACE_FILE_LIST:
    if os.path.isdir(f):
        SUB_FILE_LIST = filequery.list_all_files(f)
        DIRS_RES.append({
            'name': os.path.basename(f),
            'dir': True,
            'size': get_all_files_size(SUB_FILE_LIST)
        })
        size_max_width = max(
            len(str(DIRS_RES[-1]['size'])) + 1, size_max_width)
    if os.path.isfile(f):
        FILE_RES.append({
            'name': os.path.basename(f),
            'dir': False,
            'size': str(round(FileInfo(f).fileSize, 2))
        })
        size_max_width = max(
            len(str(FILE_RES[-1]['size'])) + 1, size_max_width)

RES.extend(DIRS_RES)
RES.extend(FILE_RES)

if SORT_OBJ_IS_NUMBER:
    RES.sort(key=lambda k: float(k.get(SORT_OBJ)), reverse=SORT_REVERSE)
else:
    RES.sort(key=lambda k: str(k.get(SORT_OBJ)), reverse=SORT_REVERSE)

idx_max_width = len(str(len(RES))) + 3

for i in range(0, len(RES)):
    font_color = 0
    if RES[i]['dir']:
        font_color = IOColors.FONT_GREEN
    else:
        font_color = IOColors.FONT_WHITE
    CustomOut(make_output_str(i + 1, RES[i], idx_max_width, size_max_width)).build(CustomOut.get_custom_color_cfg(
        IOColors.DISPLAY_DEFAULT, font_color
    )).print()
