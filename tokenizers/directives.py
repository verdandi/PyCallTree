#!/usr/bin/env python3

# developed by: Kuksov Pavel
# e-mail: aimed.fire@gmail.com

import re

from . import tokens


class IncludeSearcher:
    def __init__(self):
        self.__pattern = re.compile(r'^#include <(?P<token1>.+)>$|^#include "(?P<token2>.+)"$')
        self.__found_token = ''
        self.__token_name = ''

    def findToken(self, line):
        if not line.endswith('"') and not line.endswith('>'):
            return tokens.NOTHING_SPECIAL

        result = self.__pattern.match(line)
        if result:
            self.__found_token = line
            self.__token_name = result.group('token1') if result.groupdict()['token1'] else result.group('token2')
            return tokens.INCLUDE_DIRECTIVE
        else:
            return tokens.NOTHING_SPECIAL

    def clear(self):
        pass

    @property
    def found_token(self):
        return self.__token_name, self.__found_token


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
