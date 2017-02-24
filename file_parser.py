#!/usr/bin/env python3

# developed by: Kuksov Pavel
# e-mail: aimed.fire@gmail.com


class FileParser:
    """FileParser implements parsing of files with source code."""

    def __init__(self, tokenizers):
        self.__tokenizers = tokenizers

    def parse(self, file_name, root_directory = ''):
        full_path = root_directory + '/' + file_name if root_directory else file_name
        if full_path[-2:] != '.h' and full_path[-2:] != '.c':
            return

        for line in open(full_path, 'r'):
            for tokenizer in self.__tokenizers:
                tokenizer.findToken(line.strip())


