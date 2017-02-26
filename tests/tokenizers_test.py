#!/usr/bin/env python3

# developed by: Kuksov Pavel
# e-mail: aimed.fire@gmail.com

import unittest

from tokenizers.function import FunctionDeclarationSearcher
from tokenizers.function import FunctionDefinitionSearcher
from tokenizers.function import FunctionCallSearcher
from tokenizers.directives import IncludeSearcher
from tokenizers.directives import MacrosSearcher
from tokenizers.comments import CommentSearcher
from tokenizers import tokens


class FunctionDeclarationSearcherTest(unittest.TestCase):
    """Tests for class FunctionDeclarationSearcher"""

    def test_should_find_function_declaration(self):
        """FunctionDeclarationSearcher should find function daclaration in headers"""

        tokenizer = FunctionDeclarationSearcher()

        with open('tests/function_declaration_example2', 'r') as example:
            for i in range(0,6):
                line = example.readline()
                found_token = tokenizer.findToken(line.strip())
                self.assertEquals(tokens.NOT_ENOUGH_DATA, found_token)

            line = example.readline()
            found_token = tokenizer.findToken(line.strip())
            self.assertEquals(tokens.FUNCTION_DECLARATION, found_token)
            short_name, full_name = tokenizer.found_token
            self.assertEquals('function134', short_name)
            self.assertEquals('int function134(int val1, double val2, char* double3, void(*)(char, int, double*, int(*)() );',
                              full_name)

        with open('tests/function_declaration_example1', 'r') as example:
            line = example.readline()
            found_token = tokenizer.findToken(line.strip())

            self.assertEquals(tokens.FUNCTION_DECLARATION, found_token)
            short_name, full_name = tokenizer.found_token
            self.assertEquals('function', short_name)
            self.assertEquals(line.strip(), full_name)

    def test_can_clear_state(self):
        """FunctionDeclarationSearcher can clear state if needed"""
        tokenizer = FunctionDeclarationSearcher()


        with open('tests/function_declaration_example2', 'r') as example:
            for i in range(0,6):
                line = example.readline()
                found_token = tokenizer.findToken(line.strip())
                self.assertEquals(tokens.NOT_ENOUGH_DATA, found_token)

            tokenizer.clear()
            line = example.readline()
            found_token = tokenizer.findToken(line.strip())
            self.assertEquals(tokens.NOTHING_SPECIAL, found_token)


class FunctionDefinitionSearcherTest(unittest.TestCase):
    """Tests for class FunctionDefinitionSearcher"""

    def test_should_find_function_definition(self):
        """FunctionDefinitionSearcher should find function definition in headers"""

        tokenizer = FunctionDefinitionSearcher()

        with open('tests/function_definition_example2', 'r') as example:
            for i in range(0,6):
                line = example.readline()
                found_token = tokenizer.findToken(line.strip())
                self.assertEquals(tokens.NOT_ENOUGH_DATA, found_token)

            line = example.readline()
            found_token = tokenizer.findToken(line.strip())
            self.assertEquals(tokens.FUNCTION_DEFINITION, found_token)
            short_name, full_name = tokenizer.found_token
            self.assertEquals('function134', short_name)
            self.assertEquals('int function134(int val1, double val2, char* double3, void(*)(char, int, double*, int(*)() ){',
                              full_name)

        with open('tests/function_definition_example1', 'r') as example:
            line = example.readline()
            found_token = tokenizer.findToken(line.strip())

            self.assertEquals(tokens.FUNCTION_DEFINITION, found_token)
            short_name, full_name = tokenizer.found_token
            self.assertEquals('function', short_name)
            self.assertEquals(line.strip(), full_name)

    def test_can_clear_state(self):
        """FunctionDefinitionSearcher can clear state if needed"""
        tokenizer = FunctionDefinitionSearcher()


        with open('tests/function_definition_example2', 'r') as example:
            for i in range(0,6):
                line = example.readline()
                found_token = tokenizer.findToken(line.strip())
                self.assertEquals(tokens.NOT_ENOUGH_DATA, found_token)

            tokenizer.clear()

            line = example.readline()
            found_token = tokenizer.findToken(line.strip())
            self.assertEquals(tokens.NOTHING_SPECIAL, found_token)


class IncludeSearcherTest(unittest.TestCase):
    """Tests for class IncludeSearcher"""

    def test_should_find_include_directives(self):
        """IncludeSearcher should find include directives"""

        tokenizer = IncludeSearcher()

        with open('tests/include_example', 'r') as example:
            line = example.readline()
            found_token = tokenizer.findToken(line.strip())
            self.assertEquals(tokens.INCLUDE_DIRECTIVE, found_token)
            short_name, full_name = tokenizer.found_token
            self.assertEquals('stdio.h', short_name)
            self.assertEquals('#include <stdio.h>', full_name)

            line = example.readline()
            found_token = tokenizer.findToken(line.strip())
            self.assertEquals(tokens.INCLUDE_DIRECTIVE, found_token)
            short_name, full_name = tokenizer.found_token
            self.assertEquals('some_path/some_file.c', short_name)
            self.assertEquals('#include "some_path/some_file.c"', full_name)


class MacrosSearcherTest(unittest.TestCase):
    """Tests for class MacrosSearcher"""

    def test_should_find_macros(self):
        """MacrosSearcher should find macros"""

        tokenizer = MacrosSearcher()

        with open('tests/macros_example1', 'r') as example:
            for i in range(0,2):
                line = example.readline()
                found_token = tokenizer.findToken(line.strip())
                self.assertEquals(tokens.NOT_ENOUGH_DATA, found_token)

            line = example.readline()
            found_token = tokenizer.findToken(line.strip())
            self.assertEquals(tokens.MACROS, found_token)
            short_name, full_name = tokenizer.found_token
            self.assertEquals('NUMBERS', short_name)
            self.assertEquals("#define NUMBERS 1, \\ 2, \\3", full_name)

        with open('tests/macros_example2', 'r') as example:
            line = example.readline()
            found_token = tokenizer.findToken(line.strip())

            self.assertEquals(tokens.MACROS, found_token)
            short_name, full_name = tokenizer.found_token
            self.assertEquals('BUFFER_SIZE', short_name)
            self.assertEquals(line.strip(), full_name)

    def test_can_clear_state(self):
        """MacrosSearcher can clear state if needed"""

        tokenizer = MacrosSearcher()

        with open('tests/macros_example1', 'r') as example:
            for i in range(0,2):
                line = example.readline()
                found_token = tokenizer.findToken(line.strip())
                self.assertEquals(tokens.NOT_ENOUGH_DATA, found_token)

            tokenizer.clear()

            line = example.readline()
            found_token = tokenizer.findToken(line.strip())
            self.assertEquals(tokens.NOTHING_SPECIAL, found_token)

class CommentSearcherTest(unittest.TestCase):
    """Tests for class CommentSearcher"""

    def test_should_find_comments(self):
        """MacrosSearcher should find comments"""

        tokenizer = CommentSearcher()

        with open('tests/multiline_comment_example', 'r') as example:
            for i in range(0,3):
                line = example.readline()
                found_token = tokenizer.findToken(line.strip())
                self.assertEquals(tokens.NOT_ENOUGH_DATA, found_token)

            line = example.readline()
            found_token = tokenizer.findToken(line.strip())
            self.assertEquals(tokens.MULTILINE_COMMENT, found_token)

        with open('tests/one_line_comment_example', 'r') as example:
            line = example.readline()
            found_token = tokenizer.findToken(line.strip())
            self.assertEquals(tokens.ONELINE_COMMENT, found_token)

    def test_can_clear_state(self):
        """CommentSearcher can clear state if needed"""

        tokenizer = CommentSearcher()

        with open('tests/multiline_comment_example', 'r') as example:
            for i in range(0,3):
                line = example.readline()
                found_token = tokenizer.findToken(line.strip())
                self.assertEquals(tokens.NOT_ENOUGH_DATA, found_token)

            tokenizer.clear()

            line = example.readline()
            found_token = tokenizer.findToken(line.strip())
            self.assertEquals(tokens.NOTHING_SPECIAL, found_token)


class FunctionCallSearcherTest(unittest.TestCase):
    """Tests for class FunctionCallSearcher"""

    def test_should_find_function_calls(self):
        """FunctionCallSearcher should find function calls"""

        tokenizer = FunctionCallSearcher()

        with open('tests/function_call_example1', 'r') as example:
            line = example.readline()
            found_token = tokenizer.findToken(line.strip())
            self.assertEquals(tokens.FUNCTION_CALL, found_token)
            short_name, full_name = tokenizer.found_token
            self.assertEquals('function1', short_name)
            self.assertEquals(line.strip(), full_name)

        with open('tests/function_call_example2', 'r') as example:
            line = example.readline()
            found_token = tokenizer.findToken(line.strip())
            self.assertEquals(tokens.FUNCTION_CALL, found_token)
            short_name, full_name = tokenizer.found_token
            self.assertEquals('function2', short_name)
            self.assertEquals(line.strip(), full_name)

        with open('tests/function_call_example3', 'r') as example:
            for i in range(0,2):
                line = example.readline()
                found_token = tokenizer.findToken(line.strip())
                self.assertEquals(tokens.NOT_ENOUGH_DATA, found_token)

            line = example.readline()
            found_token = tokenizer.findToken(line.strip())
            self.assertEquals(tokens.FUNCTION_CALL, found_token)
            short_name, full_name = tokenizer.found_token
            self.assertEquals('function3', short_name)
            self.assertEquals('int val = function3( 5, "some string");', full_name)

        with open('tests/function_call_example4', 'r') as example:
            for i in range(0,5):
                line = example.readline()
                found_token = tokenizer.findToken(line.strip())
                self.assertEquals(tokens.NOT_ENOUGH_DATA, found_token)

            line = example.readline()
            found_token = tokenizer.findToken(line.strip())
            self.assertEquals(tokens.FUNCTION_CALL, found_token)
            short_name, full_name = tokenizer.found_token
            self.assertEquals('function4', short_name)
            self.assertEquals(' function4(val1, val2, val3 ) ){', full_name)


    def test_can_check_the_same_line_after_found_call(self):
        """FunctionCallSearcher can check the same line after found call"""

        tokenizer = FunctionCallSearcher()

        with open('tests/function_call_example5', 'r') as example:
            line = example.readline()
            found_token = tokenizer.findToken(line.strip())
            self.assertEquals(tokens.FUNCTION_CALL, found_token)
            short_name, full_name = tokenizer.found_token
            self.assertEquals('function5', short_name)
            self.assertEquals(line.strip(), full_name)

            the_same_line = line.strip()
            the_same_line = the_same_line[the_same_line.find('(')+1:]
            found_token = tokenizer.findToken(the_same_line)
            self.assertEquals(tokens.FUNCTION_CALL, found_token)
            short_name, full_name = tokenizer.found_token
            self.assertEquals('function6', short_name)
            tokenizer.clear()


if __name__ == '__main__':
    unittest.main()
