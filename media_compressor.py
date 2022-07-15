import os

import configparser
import sys

from default import config
from modules import filequery, charparser, compressor
from pathlib import Path

config_parser = configparser.ConfigParser()


def addComment(file_name, section, comment):
    content = ''
    for line in open(file_name, encoding='utf-8'):
        if ('[' + section + ']') in line:
            content += ';' + comment + '\n'
        content += line
    comment_writer = open(file_name, 'w', encoding='utf-8')
    comment_writer.write(content)
    comment_writer.close()


def createConfByDefault(preset, conf_path):
    for i in range(len(preset.SECTIONS)):
        config_parser.add_section(preset.SECTIONS[i])
        for j in range(len(preset.SECTIONS_CONF_NAME[i])):
            config_parser.set(
                preset.SECTIONS[i], preset.SECTIONS_CONF_NAME[i][j], preset.SECTIONS_CONF_VALUE[i][j])
    config_parser.write(open(conf_path, 'w', encoding='utf-8'))
    for i in range(len(preset.SECTIONS)):
        for comment in preset.SECTIONS_COMMENT[i]:
            addComment(conf_path, preset.SECTIONS[i], comment)


def unknownParam(option: str):
    print("error: Unrecognized target \"" + option + '\"')
    exit(1)


def printHelp():
    print("Usage: " + sys.argv[0] + " {Type} {Addon}")
    print("     - Type: video, image")
    print("     - [Optional]Addon: genconf(Only generate config file)")
    exit(0)


_CONF_PRESET = ''
_COMPRESS_TARGET = ''
_CONFIG_PATH = ''

if len(sys.argv) > 1:
    if sys.argv[1] == 'video':
        _CONF_PRESET = config.VideoConf
    elif sys.argv[1] == 'image':
        _CONF_PRESET = config.ImageConf
    elif sys.argv[1] == 'help':
        printHelp()
    else:
        unknownParam(sys.argv[1])
    _COMPRESS_TARGET = sys.argv[1]
    _CONFIG_PATH = "toolbox_" + sys.argv[1] + ".ini"
    if len(sys.argv) > 2:
        if sys.argv[2] == 'genconf':
            if Path(_CONFIG_PATH).exists():
                os.remove(_CONFIG_PATH)
            createConfByDefault(_CONF_PRESET, _CONFIG_PATH)
            print("Generate \'" + _CONFIG_PATH + "\' config file")
            exit(0)
        else:
            unknownParam(sys.argv[2])
else:
    printHelp()
if not Path(_CONFIG_PATH).exists():
    createConfByDefault(_CONF_PRESET, _CONFIG_PATH)
config_parser.read(_CONFIG_PATH, 'utf-8')

_INPUT_FORMAT = config_parser.get('IO_FORMAT', 'input').split('|')
_INPUT_DIR = charparser.parse_path(
    config_parser.get('IO_DIR', 'input'), os.getcwd())
if _INPUT_DIR == 'none':
    _INPUT_DIR = os.getcwd()
_FILE_LIST = filequery.search_by_ext(
    filequery.list_all_files(_INPUT_DIR), _INPUT_FORMAT)

TASK_CNT = 0
for FILE in _FILE_LIST:
    TASK_CNT += 1
    compressor.compress(config_parser, FILE, TASK_CNT, _COMPRESS_TARGET)
