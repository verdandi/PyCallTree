#!/usr/bin/env python3

# developed by: Kuksov Pavel
# e-mail: aimed.fire@gmail.com

import unittest

from file_walker import FileWalker

class FileWalkerTest(unittest.TestCase):
    """Tests for class FileWalker"""

    def test_should_find_all_files_in_directory(self):
        """FileWalker should find all files in given directory"""

        files = ['./file1', './dir1/file2', './dir1/file3', './dir1/dir2/file4', './dir1/dir3/file5', './dir1/dir3/file6']
        found_files = []
        for file_name in FileWalker('tests/dir_tree_example'):
            found_files.append(file_name)

        self.assertListEqual(found_files, files)
