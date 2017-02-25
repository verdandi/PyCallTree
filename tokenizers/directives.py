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
