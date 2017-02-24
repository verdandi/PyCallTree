#!/usr/bin/env python3

# developed by: Kuksov Pavel
# e-mail: aimed.fire@gmail.com

from tokenizers import tokens


class FileParser:
    """FileParser implements parsing of files with source code."""

    def __init__(self, tokenizers):
        self.__tokenizers = tokenizers
        self.__tokens_map = {}

    def parse(self, file_name, root_directory = ''):
        full_path = root_directory + '/' + file_name if root_directory else file_name
        if full_path[-2:] != '.h' and full_path[-2:] != '.c':
            return

        for number, line in enumerate(open(full_path, 'r'), start = 1):
            for tokenizer in self.__tokenizers:
                token = tokenizer.findToken(line.strip())
                if token == tokens.FUNCTION_DECLARATION:
                    self.__tokens_map.setdefault(
                        tokenizer.found_token, {'declarations': [], 'definitions': []})['declarations'].append(
                        file_name+':'+str(number))

    @property
    def tokens_map(self):
        return self.__tokens_map
