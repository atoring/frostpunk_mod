#!/usr/bin/python
# coding: utf-8

import codecs
import os
import urllib.request

from common import *

_sheet_url  = "https://docs.google.com/spreadsheets/d/1-eu8GT6_zI4IOTHWFymplV81GJj1Q469FSWv6jGUHH8/export?format=csv&gid=2068465123"
_sheet_path = "./data"
_sheet_file = "Frostpunk 翻訳作業所 - 翻訳.csv"

class Sheet():
    "japanese translation sheet"

    def __init__(self):
        "constructor"
        path = os.path.join(get_prog_path(), _sheet_path)
        path = path.replace("/", os.sep)
        self.__sheet_path = path
        path = os.path.join(path, _sheet_file)
        self.__sheet_file = path

    def fetch(self):
        "fetch sheet from web site"
        log("fetch sheet", _sheet_url)
        try:
            data = urllib.request.urlopen(_sheet_url).read().decode("utf-8")
        except:
            log("error", "fetch sheet", _sheet_url)
            return False
        if not make_dir(self.__sheet_path):
            return False
        return write_txt(self.__sheet_file, data)

    @property
    def exists(self):
        "check exsits sheet file"
        return os.path.isfile(self.__sheet_file)

    @property
    def sheet_path(self):
        "get backup path"
        return self.__sheet_file
