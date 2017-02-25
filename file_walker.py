#!/usr/bin/env python3

# developed by: Kuksov Pavel
# e-mail: aimed.fire@gmail.com


import os
from collections import deque


class FileWalker:
    """Class FileWalker recursivelly finds all files in given dir and all subdirs"""

    def __init__(self, root):
        self.__root = root
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
