import sys


class IOColors:
    DISPLAY_DEFAULT = 0
    DISPLAY_HIGHLIGHT = 1
    DISPLAY_UNDERLINE = 4
    DISPLAY_FLICKER = 5
    DISPLAY_REVERSE_COLOR = 7
    DISPLAY_HIDDEN = 8

    FONT_BLACK = 30
    FONT_RED = 31
    FONT_GREEN = 32
    FONT_YELLOW = 33
    FONT_BLUE = 34
    FONT_FUCHSIA = 35
    FONT_CYAN = 36
    FONT_WHITE = 37

    BACKGROUND_BLACK = 40
    BACKGROUND_RED = 41
    BACKGROUND_GREEN = 42
    BACKGROUND_YELLOW = 43
    BACKGROUND_BLUE = 44
    BACKGROUND_FUCHSIA = 45
    BACKGROUND_CYAN = 46
    BACKGROUND_WHITE = 47


class CustomOut:
    __output = ''

    @staticmethod
    def get_custom_color_cfg(self, display=IOColors.DISPLAY_DEFAULT, font=IOColors.FONT_WHITE,
                             background=IOColors.BACKGROUND_BLACK) -> dict:
        return {
            'display': display,
            'font': font,
            'background': background
        }

    def set(self, content: str):
        self.__output = content
        return self

    def build(self, color_cfg=None):
        if color_cfg is not None and type(dict()) == type(color_cfg):
            if 'display' in color_cfg.keys() and \
                    'font' in color_cfg.keys() and \
                    'background' in color_cfg.keys():
                self.__output = "\033[{display};{font};{background}m{content}\033[0m".format(
                    display=color_cfg['display'], font=color_cfg['font'], background=color_cfg['background'],
                    content=self.__output)
        return self

    def print(self, end='\n'):
        print(self.__output, end=end)
        self.__output = ''
