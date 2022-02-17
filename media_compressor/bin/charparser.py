import os
import sys


def Bool(value: str):
    value = value.lower()
    if value == 'true':
        return True
    elif value == 'false':
        return False
    else:
        print("error: \"" + value + "\" is not a bool value, it's may a typo, please check your config")
        exit(1)


def get_path_delimiter():
    if 'win' in sys.platform:
        return '\\'
    elif 'mac' in sys.platform or 'linux' in sys.platform:
        return '/'
    else:
        print("error: Unrecognized platform " + sys.platform + " or not support")
        exit(1)


def parse_path(path: str):
    if path == 'none':
        return path
    if path[0] != '[':
        print("error: \"" + path + "\" is not a legal path. For more information, please check notes in .ini file")
        exit(1)
    start: int = 1
    end: int = 0
    for i in range(len(path)):
        if path[i] == ']':
            end = i
            break
    if path[start:end] == 'absolute':
        return path[end + 1:]
    elif path[start:end] == 'relative':
        return os.getcwd() + get_path_delimiter() + path[end + 1:]
    else:
        print("error: \"" + path[0:end + 1] + "\" is unrecognized, it's may a typo. For more information"
                                              ", please check notes in .ini file")
        exit(1)
