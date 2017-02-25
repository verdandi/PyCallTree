#!/usr/bin/env python3

# developed by: Kuksov Pavel
# e-mail: aimed.fire@gmail.com

import re

from . import tokens


class FunctionDeclarationSearcher:
    def __init__(self):
        self.__pattern = re.compile(r'^static \w+ (?P<token1>\w+)\(.*\);$|^\w+ (?P<token2>\w+)\(.*\);$')
        self.__found_token = ''
        self.__token_name = ''
        self.__data_part = ''

    def findToken(self, line):
        if not line.endswith(';'):
            if not self.__data_part:
                self.__data_part = line
            else:
                self.__data_part = ' '.join([self.__data_part, line])
            return tokens.NOT_ENOUGH_DATA

        test_string = self.__data_part + line
        result = self.__pattern.match(test_string)
        if result:
            self.__found_token = test_string
            self.__token_name = result.group('token1') if result.groupdict()['token1'] else result.group('token2')
            self.__data_part = ''
            return tokens.FUNCTION_DECLARATION
        else:
            self.__data_part = ''
            return tokens.NOTHING_SPECIAL

    @property
    def found_token(self):
        return self.__token_name, self.__found_token
