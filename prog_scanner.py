import os
import platform
import sys

WIN32_SEP = "\\"
WIN32_DOUBLE_SEP = WIN32_SEP + WIN32_SEP
LINUX_DRAWIN_SEP = "/"

WIN32_EXECUTABLE_SUFFIX = '.exe'

IS_WSL = os.getenv('WSL_DISTRO_NAME') is not None

def get_default_execuatable_suffix():
    ret = []
    if sys.platform == 'win32':
        ret.append(WIN32_EXECUTABLE_SUFFIX)
    else:
        ret.append('')
    if IS_WSL:
        ret.append(WIN32_EXECUTABLE_SUFFIX)
    return ret

def get_path_env_sep():
    if sys.platform == 'win32':
        return ';'
    else:
        return ':'

def get_sep():
    if sys.platform == 'win32':
        return WIN32_SEP
    else:
        return LINUX_DRAWIN_SEP

if len(sys.argv) != 2:
    print("Usage: python3 prog_scanner.py <program name>")
    sys.exit(1)

PATH_ENV = os.getenv('PATH')
PATH_ARR = PATH_ENV.split(get_path_env_sep())

PROG_NAME = sys.argv[1]
PROG_PATH = None

for i in PATH_ARR:
    if not i.endswith(get_sep()):
        i += get_sep()
    for j in get_default_execuatable_suffix():
        if os.path.isfile(i + PROG_NAME + j):
            PROG_PATH = i + PROG_NAME + j
            break
    if PROG_PATH is not None:
        break

if PROG_PATH is not None:
    print("找到程序%s" % PROG_NAME)
    print("路径: %s" % PROG_PATH)
    if PROG_PATH.endswith(WIN32_EXECUTABLE_SUFFIX) and IS_WSL:
        print("警告: 此程序是在WSL环境下检测到的Windows可执行程序, 可能无法在此环境下正常运行")
else:
    print("未找到程序%s" % PROG_NAME)