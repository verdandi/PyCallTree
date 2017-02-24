#!/usr/bin/env python3

# developed by: Kuksov Pavel
# e-mail: aimed.fire@gmail.com


import unittest

from . import tokenizer_mock
from file_parser import FileParser


class FileParserTest(unittest.TestCase):
    """Tests for class FaileParser."""

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


