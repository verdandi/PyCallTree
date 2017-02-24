#!/usr/bin/env python3

# developed by: Kuksov Pavel
# e-mail: aimed.fire@gmail.com

import unittest
import colour_runner.runner

from tests import tokenizers_test
from tests import file_walker_test
from tests import file_parser_test

loader = unittest.TestLoader()

suite = loader.loadTestsFromModule(tokenizers_test)
suite.addTests(loader.loadTestsFromModule(file_walker_test))
suite.addTests(loader.loadTestsFromModule(file_parser_test))

r = colour_runner.runner.ColourTextTestRunner(verbosity = 2)
result = r.run(suite)
