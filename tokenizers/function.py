#!/usr/bin/env python3

# developed by: Kuksov Pavel
# e-mail: aimed.fire@gmail.com

import re

from . import tokens


class FunctionDeclarationSearcher:
    def __init__(self):
        self.__pattern = re.compile(r'^static \w+ (?P<token1>\w+)\(.*\) *;$|^\w+ (?P<token2>\w+)\(.*\) *;$')
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

    def clear(self):
        self.__data_part = ''

    @property
    def found_token(self):
        return self.__token_name, self.__found_token

class FunctionDefinitionSearcher:
    def __init__(self):
        self.__pattern = re.compile(r'^static \w+ (?P<token1>\w+)\(.*\) *{$|^\w+ (?P<token2>\w+)\(.*\) *{$')
        self.__found_token = ''
        self.__token_name = ''
        self.__data_part = ''

    def findToken(self, line):
        if not line.endswith('{'):
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
            return tokens.FUNCTION_DEFINITION
        else:
            self.__data_part = ''
            return tokens.NOTHING_SPECIAL

    def clear(self):
        self.__data_part = ''

    @property
    def found_token(self):
        return self.__token_name, self.__found_token


class FunctionCallSearcher:
    key_words = ('if', 'switch', 'while', 'for')

    def __init__(self):
        self.__pattern = re.compile(r'^ *(?P<token1>\w+)\(.*\) *\)*[{;]$|^.*[,=] *(?P<token2>\w+)\(.*\) *\)*[{;]$')
        self.__found_token = ''
        self.__token_name = ''
        self.__data_part = ''

    def excludeKeyWords(self, line):
        hightest_key_word_position = 0

        for key_word in FunctionCallSearcher.key_words:
            pos = line.rfind(key_word)
            pos = pos+len(key_word) if pos >= 0 else pos
            hightest_key_word_position = max(hightest_key_word_position, pos)

        if hightest_key_word_position == 0:
            return line

        position_of_bracket_after_key_word = line.find('(', hightest_key_word_position)
        return line[position_of_bracket_after_key_word+1:]

    def findToken(self, line):
        if not line.endswith('{') and not line.endswith(';'):
            if not self.__data_part:
                self.__data_part = line
            else:
                self.__data_part = ' '.join([self.__data_part, line])
            return tokens.NOT_ENOUGH_DATA

        test_string = self.excludeKeyWords(self.__data_part + line)

        result = self.__pattern.match(test_string)
        if result:
            self.__found_token = test_string
            self.__token_name = result.group('token1') if result.groupdict()['token1'] else result.group('token2')
            self.__data_part = ''
            return tokens.FUNCTION_CALL
        else:
            self.__data_part = ''
            return tokens.NOTHING_SPECIAL

    # def checkOneMoreTime(self):
        # print("\n---- ", self.__found_token)
        # result = self.__pattern.match(self.__found_token)
        # if result:
            # self.__token_name = result.group('token1') if result.groupdict()['token1'] else result.group('token2')
            # return tokens.FUNCTION_CALL
        # else:
            # return tokens.NOTHING_SPECIAL

    def clear(self):
        self.__data_part = ''

    @property
    def found_token(self):
        # found_token_name = self.__token_name
        # full_string = self.__found_token
        # self.__found_token = self.__found_token[self.__found_token.find('(')+1:]
        # return found_token_name, full_string
        return self.__token_name, self.__found_token
