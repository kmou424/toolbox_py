import locale as loca
import os
from pathlib import Path


def get_default_language():
    lang, __ = loca.getdefaultlocale()
    if lang is None:
        return 'en_US'
    return lang


class Language:
    def __init__(self, target_lang: str, default_lang: str):
        self.lang_dict = {}
        dirname, __ = os.path.split(os.path.abspath(__file__))
        target_lang: Path = Path(dirname) / ("%s.lang" % target_lang)
        default_lang: Path = Path(dirname) / ("%s.lang" % default_lang)
        if default_lang.exists():
            self.__load_from_file(default_lang)
        if target_lang.absolute() != default_lang.absolute() and target_lang.exists():
            self.__load_from_file(target_lang)

    def __load_from_file(self, lang_file: Path):
        lines = lang_file.read_text(encoding='utf-8').split('\n')
        for line in lines:
            idx = line.find('=')
            if line == '' or line.startswith('#'):
                continue
            if idx == -1:
                break
            key = line[0:idx]
            content = line[idx+1:]
            if content.startswith('\'') or content.startswith('\"'):
                content = content[1:]
            else:
                break
            if content.endswith('\'') or content.endswith('\"'):
                content = content[:-1]
            else:
                break
            self.lang_dict[key] = content

    def get_string(self, key: str) -> str:
        if key not in self.lang_dict.keys():
            return 'Error: Can not find the key \'%s\', please check .lang files in locale directory' % key
        return self.lang_dict[key]
