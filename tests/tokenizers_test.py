#!/usr/bin/env python3

# developed by: Kuksov Pavel
# e-mail: aimed.fire@gmail.com

import unittest

from tokenizers.function import FunctionDeclarationSearcher
from tokenizers.function import tokens

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


if __name__ == '__main__':
    unittest.main()
