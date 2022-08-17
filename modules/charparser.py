import os
import sys


def Bool(value: str):
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
        print("error: \"" + value +
              "\" is not a bool value, it's may a typo, please check your config")
        exit(1)


def get_path_delimiter():
    if 'win' in sys.platform:
        return '\\'
    elif 'mac' in sys.platform or 'linux' in sys.platform:
        return '/'
    else:
        print("error: Unrecognized platform " +
              sys.platform + " or not support")
        exit(1)


def replace_variables(path: str, variables: dict):
    for key in variables:
        path = path.replace('{' + key + '}', variables[key])
    return path


def parse_path(path: str, ori_filepath: str):
    if path == 'none':
        return path
    if path[0] != '[':
        print("error: \"" + path +
              "\" is not a legal path. For more information, please check notes in .ini file")
        exit(1)
    start: int = 1
    end: int = 0
    for i in range(len(path)):
        if path[i] == ']':
            end = i
            break
    if path.endswith('\\'):
        path.rstrip('\\')

    ori_dirname_list = os.path.dirname(
        ori_filepath).split(get_path_delimiter())
    # replace preset variables
    preset_variables = dict()
    preset_variables['src_dir'] = ori_dirname_list[-1]
    path = replace_variables(path, preset_variables)

    path_head = path[start:end]
    path_body = path[end+1:]

    if path_head == 'absolute':
        return path[end + 1:]
    elif path_head == 'relative':
        while path_body.startswith('..\\') or path_body.startswith('../'):
            path_body = path_body[3:]
            ori_dirname_list = ori_dirname_list[:-1]
        ori_dirname = get_path_delimiter().join(ori_dirname_list)
        return ori_dirname + get_path_delimiter() + path_body
    elif path_head == 'source':
        return os.path.dirname(ori_filepath)
    else:
        print("error: \"" + path_head + "\" is unrecognized, it's may a typo. For more information"
              ", please check notes in .ini file")
        exit(1)
