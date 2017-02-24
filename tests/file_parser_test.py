#!/usr/bin/env python3

# developed by: Kuksov Pavel
# e-mail: aimed.fire@gmail.com


import unittest

from . import tokenizer_mock
from file_parser import FileParser
from tokenizers import function


class FileParserTest(unittest.TestCase):
    """Tests for class FileParser."""

    def test_should_ignore_file_if_it_is_not_source_file(self):
        """FileParser should ignore file if it is not source file."""

        tokenizer = tokenizer_mock.TokenizerMock()
        tokenizers = [tokenizer]
        parser = FileParser(tokenizers)
        parser.parse('./tests/function_declaration_example1')

        self.assertListEqual(tokenizer.received_strings, [])

        parser.parse('./tests/header_example.h')
        readed_lines = []
        for line in open('./tests/header_example.h'):
            readed_lines.append(line.strip())

        self.assertListEqual(tokenizer.received_strings, readed_lines)

    def test_should_save_found_tokens(self):
        """FileParser should save found tokens."""

        tokenizer = function.FunctionDeclarationSearcher()
        tokenizers = [tokenizer]
        parser = FileParser(tokenizers)

        parser.parse('./tests/header_example.h')

        tokens_map = parser.tokens_map
        locations = tokens_map['int function134(int val1, double val2, char* double3, void(*)(char, int, double*, int(*)() );']
        self.assertListEqual(locations['declarations'], ['./tests/header_example.h:11'])
        self.assertListEqual(locations['definitions'], [])

