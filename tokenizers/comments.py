#!/usr/bin/env python3

# developed by: Kuksov Pavel
# e-mail: aimed.fire@gmail.com

from . import tokens


class CommentSearcher:
    def __init__(self):
        self.__is_multiline_comment_found = False

    def findToken(self, line):
        if not self.__is_multiline_comment_found and not line.startswith('//') and not line.startswith('/*'):
            return tokens.NOTHING_SPECIAL

        if line.startswith('//'):
            return tokens.ONELINE_COMMENT

        if not self.__is_multiline_comment_found and line.startswith('/*'):
            self.__is_multiline_comment_found = True
            return tokens.NOT_ENOUGH_DATA

        if self.__is_multiline_comment_found and not line.endswith('*/'):
            return tokens.NOT_ENOUGH_DATA

        if self.__is_multiline_comment_found and line.endswith('*/'):
            self.__is_multiline_comment_found = False
            return tokens.MULTILINE_COMMENT

    def clear(self):
        self.__is_multiline_comment_found = False

    @property
    def found_token(self):
        pass


class MacrosSearcher:
    def __init__(self):
        self.__pattern = re.compile(r'^#define (?P<token>\w+).*$')
        self.__found_token = ''
        self.__token_name = ''
        self.__data_part = ''

    def findToken(self, line):
        if not line.startswith('#define') and not self.__data_part:
            return tokens.NOTHING_SPECIAL

        if line.endswith('\\'):
            if not self.__data_part:
                self.__data_part = line
            else:
                self.__data_part = ' '.join([self.__data_part, line])
            return tokens.NOT_ENOUGH_DATA

        test_string = self.__data_part + line
        result = self.__pattern.match(test_string)
        if result:
            self.__found_token = test_string
            self.__token_name = result.group('token')
            self.__data_part = ''
            return tokens.MACROS
        else:
            self.__data_part = ''
            return tokens.NOTHING_SPECIAL

    def clear(self):
        self.__data_part = ''

    @property
    def found_token(self):
        return self.__token_name, self.__found_token
