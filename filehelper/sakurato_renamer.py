import os
import sys


# [文件整理]用于批量自动重命名夜樱字幕组的作品


def check_similarity(str1: str, str2: str, similarity: int):
    simi = find_max_common_substr(str1, str2)
    return len(simi) > similarity


def find_max_common_substr(s1, s2):
    m = [[0 for _i in range(len(s2) + 1)] for _ in range(len(s1) + 1)]
    max_len = 0
    p = 0
    for _i in range(len(s1)):
        for j in range(len(s2)):
            if s1[_i] == s2[j]:
                m[_i + 1][j + 1] = m[_i][j] + 1
                if m[_i + 1][j + 1] > max_len:
                    max_len = m[_i + 1][j + 1]
                    p = _i + 1
    return s1[p - max_len:p]


def get_path_delimiter():
    if 'win' in sys.platform:
        return '\\'
    elif 'mac' in sys.platform or 'linux' in sys.platform:
        return '/'
    else:
        print("error: Unrecognized platform " +
              sys.platform + " or not support")
        exit(1)


def renameAnimeDir(path: str):
    dir_list = os.listdir(path)
    dir_list.sort(key=lambda p: len(p), reverse=True)
    if len(dir_list) >= 2:
        cmp_str = ""
        for _i in range(len(dir_list)):
            if dir_list[_i] == "前作":
                print("Note: {path}{delimiter}{basename}"
                      .format(path=path, delimiter=get_path_delimiter(), basename=dir_list[_i]))
            if dir_list[_i].__contains__('] '):
                old_sub_dir_name = "{dirname}{delimiter}{subdir}" \
                    .format(dirname=path,
                            delimiter=get_path_delimiter(),
                            subdir=dir_list[_i])
                new_sub_dirname = "{dirname}{delimiter}{subdir}" \
                    .format(dirname=path,
                            delimiter=get_path_delimiter(),
                            subdir=dir_list[_i].replace('] ', ']'))
                if old_sub_dir_name != new_sub_dirname:
                    os.rename(old_sub_dir_name, new_sub_dirname)
                    print("Detected illegal filename, rename it:\n"
                          "    Old name:\n"
                          "    {old}\n"
                          "    New name:\n"
                          "    {new}\n".format(old=old_sub_dir_name, new=new_sub_dirname))
            if check_similarity(os.path.basename(path), dir_list[_i], 4):
                if dir_list[_i] != os.path.basename(path):
                    cmp_str = dir_list[_i]
        if cmp_str != os.path.basename(path) and cmp_str != "":
            max_common_substr = find_max_common_substr(
                cmp_str, os.path.basename(path))

            if max_common_substr.startswith(']') or max_common_substr.startswith('}'):
                max_common_substr = max_common_substr[1:]
            new_path = "{dirname}{delimiter}{max_common_substr}" \
                .format(dirname=os.path.dirname(path),
                        delimiter=get_path_delimiter(),
                        max_common_substr=max_common_substr)
            os.rename(path, new_path)
            print("Folder name changed:\n"
                  "    Old name:\n"
                  "    {old}\n"
                  "    New name:\n"
                  "    {new}\n".format(old=path, new=new_path))


PWD = os.getcwd()
DIR_LIST = os.listdir(PWD)

for i in DIR_LIST:
    print()
    print("Processing: {root}{delimiter}{dir}".format(
        root=PWD, delimiter=get_path_delimiter(), dir=i))
    renameAnimeDir("{root}{delimiter}{dir}".format(
        root=PWD, delimiter=get_path_delimiter(), dir=i))
