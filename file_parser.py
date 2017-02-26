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
