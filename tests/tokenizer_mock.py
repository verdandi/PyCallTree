#!/usr/bin/env python3

# developed by: Kuksov Pavel
# e-mail: aimed.fire@gmail.com


class TokenizerMock:
    """TokenizerMock is mock object which implements interface of tokenizers."""

    def __init__(self):
        self.__received_strings = []

    def findToken(self, line):
        self.__received_strings.append(line)

    @property
    def received_strings(self):
        return self.__received_strings
