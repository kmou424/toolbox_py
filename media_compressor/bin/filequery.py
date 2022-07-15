def search_by_ext(_list: list, _ext_list: list):
    _result = []
    for ext in _ext_list:
        for item in _list:
            if str(item).endswith('.' + ext):
                _result.append(str(item))
    return _result


def list_all_files(directory, depth=None):
    import os
    if depth is not None:
        if depth == 0:
            return []
        depth = depth - 1
    _files = []
    _list = list_files_and_directories(directory)
    for i in range(0, len(_list)):
        path = os.path.join(directory, _list[i])
        if os.path.isdir(path):
            _files.extend(list_all_files(path, depth))
        if os.path.isfile(path):
            _files.append(path)
    return _files


def list_files_and_directories(directory: str):
    import os
    return os.listdir(directory)
