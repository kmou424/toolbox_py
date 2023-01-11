import configparser
import os
import sys
from pathlib import Path

from default import config
from language.locale_base import Language, get_default_language
from modules import filequery, charparser, compressor
from modules.cleaner import clean_relative_files, create_relative_files, PASS_MODE_LOG_FILES, PASS_MODE_MBTREE_FILES

config_parser = configparser.ConfigParser()
lang = Language(get_default_language(), 'en_US')


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
PWD = os.getcwd()

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
        for i in range(2, len(sys.argv)):
            if sys.argv[i] == 'genconf':
                if Path(_CONFIG_PATH).exists():
                    os.remove(_CONFIG_PATH)
                createConfByDefault(_CONF_PRESET, _CONFIG_PATH)
                print("Generate \'" + _CONFIG_PATH + "\' config file")
                exit(0)
            elif sys.argv[i].startswith('-c=') or sys.argv[i].startswith('--config='):
                CMDLINE_CONFIG_PATH = sys.argv[i].removeprefix('-c=').removeprefix('--config=')
                while CMDLINE_CONFIG_PATH.startswith('\"') or CMDLINE_CONFIG_PATH.startswith('\''):
                    CMDLINE_CONFIG_PATH = CMDLINE_CONFIG_PATH.removeprefix('\"').removeprefix('\'')
                while CMDLINE_CONFIG_PATH.endswith('\"') or CMDLINE_CONFIG_PATH.endswith('\''):
                    CMDLINE_CONFIG_PATH = CMDLINE_CONFIG_PATH.removesuffix('\"').removesuffix('\'')
                if os.path.exists(CMDLINE_CONFIG_PATH):
                    _CONFIG_PATH = CMDLINE_CONFIG_PATH
            else:
                unknownParam(sys.argv[i])
else:
    printHelp()
if not Path(_CONFIG_PATH).exists():
    createConfByDefault(_CONF_PRESET, _CONFIG_PATH)

print(lang.get_string('CONFIG_PATH_NOTICE') % Path(_CONFIG_PATH).absolute())
config_parser.read(_CONFIG_PATH, 'utf-8')

_INPUT_FORMAT = [_.lower() for _ in config_parser.get('IO_FORMAT', 'input').split('|')]
_INPUT_DIRS = charparser.parse_path(config_parser.get('IO_DIR', 'input'), PWD).split('|')
if _INPUT_DIRS == 'none':
    _INPUT_DIRS = [PWD]

# 多重推导式 为每个输入目录计算忽略目录
_IGNORE_DIRS = [charparser.parse_path(i, j)
                for i in config_parser.get('IO_DIR', 'ignore_input').split('|')
                for j in _INPUT_DIRS]

_TODO_FILES = []
for input_dir in _INPUT_DIRS:
    # 为每个输入目录查找并排序
    _EXT_TODO_FILES = filequery.search_by_ext(filequery.list_all_files(input_dir), _INPUT_FORMAT)
    _EXT_TODO_FILES.sort()
    _TODO_FILES.extend(_EXT_TODO_FILES)

for ignore in _IGNORE_DIRS:
    _NEW_TODO_FILES = []
    for file in _TODO_FILES:
        if file.startswith(ignore):
            print(lang.get_string("IGNORE_INPUT_NOTICE_HEAD"), file)
        else:
            _NEW_TODO_FILES.append(file)
    _TODO_FILES = _NEW_TODO_FILES

# Pass mode prepare
if _COMPRESS_TARGET == 'video' and 'pass' in config_parser.get('TARGET_ENCODER_OPTION', 'mode'):
    log_file_list = []
    for f in PASS_MODE_LOG_FILES:
        # Special judgement: Only create log file not temp file
        if not f.endswith('.temp'):
            log_file_list.append(f)
    create_relative_files(log_file_list)

TASK_CNT = 0
for FILE in _TODO_FILES:
    TASK_CNT += 1
    compressor.compress(config_parser, FILE, TASK_CNT, _COMPRESS_TARGET, TASK_CNT == len(_TODO_FILES))

if _COMPRESS_TARGET == 'video' and 'pass' in config_parser.get('TARGET_ENCODER_OPTION', 'mode'):
    clean_relative_files(PASS_MODE_MBTREE_FILES)
