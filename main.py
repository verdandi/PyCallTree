#!/usr/bin/env python3

# developed by: Kuksov Pavel
# e-mail: aimed.fire@gmail.com

import os
from collections import deque

from tokenizers import tokens


class FileWalker:
    """Class FileWalker recursivelly finds all files in given dir and all subdirs"""

    def __init__(self, root):
        self.__root = root[:len(root)-1] if root.endswith('/') else root
        self.__walker = os.walk(root)
        self.__current_dir = root
        self.__found_dirs = []
        self.__found_files = []

    def __iter__(self):
        return self

    def __next__(self):
        while not self.__found_files:
            self.__current_dir, self.__found_dirs, self.__found_files = next(self.__walker)
            if self.__current_dir == self.__root:
                self.__current_dir = ''
            else:
                self.__current_dir = self.__current_dir.replace(self.__root+'/', '')
            self.__found_files = deque(self.__found_files)

        found_file = self.__found_files.popleft();
        if not self.__current_dir:
            return found_file
        else:
            return self.__current_dir + '/' + found_file


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
            # we try to skip ends of functions or some expressions
            if (line.strip() == '}' or (line.startswith('#') and (line.find("ifdef") >= 0 or
                line.find("endif") >= 0 or line.find("if") >= 0 or line.find("else") >= 0 or
                line.find("undef") >= 0))):
                continue

            for tokenizer in self.__tokenizers:
                token = tokenizer.findToken(line.strip())
                if token == tokens.FUNCTION_DECLARATION:
                    token_name, detailed_name = tokenizer.found_token
                    new_token = self.__tokens_map.setdefault(token_name, {'detail': '', 'declarations': [], 'definitions': []})
                    new_token['detail'] = detailed_name
                    new_token['declarations'].append(file_name+':'+str(number))
                    self.clearTokenizers()

                if token == tokens.FUNCTION_DEFINITION:
                    token_name, detailed_name = tokenizer.found_token
                    new_token = self.__tokens_map.setdefault(token_name, {'detail': '', 'declarations': [], 'definitions': []})
                    if not new_token['detail']:
                        new_token['detail'] = detailed_name

                    new_token['definitions'].append(file_name+':'+str(number))
                    self.clearTokenizers()

                if token == tokens.INCLUDE_DIRECTIVE:
                    self.clearTokenizers()

                if token == tokens.MACROS:
                    self.clearTokenizers()

                if token == tokens.ONELINE_COMMENT:
                    self.clearTokenizers()

                if token == tokens.MULTILINE_COMMENT:
                    self.clearTokenizers()

        self.clearTokenizers()

    def clearTokenizers(self):
        for tokenizer in self.__tokenizers:
            tokenizer.clear()

    @property
    def tokens_map(self):
        return self.__tokens_map
