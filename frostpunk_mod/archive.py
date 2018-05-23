#!/usr/bin/python
# coding: utf-8

from common import *

_index_ext  = ".idx"
_data_ext   = ".dat"

class File():
    "file"

    def __init__(self):
        "constructor"

class Archive():
    "idx+dat archive"

    def __init__(self):
        "constructor"

    def read_archive(self, path):
        "open idx file"
        log("open idx file", path)
        self.__path         = path
        self.__index_path   = path + _index_ext
        self.__data_path    = path + _data_ext

    def write_archive(self, path):
        "write idx+dat archive"

    def get_file(self, id):
        "get file from archive"

    def set_file(self, id, data):
        "set file to archive"
