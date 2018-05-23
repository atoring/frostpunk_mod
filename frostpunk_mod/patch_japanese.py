#!/usr/bin/python
# coding: utf-8

import codecs
import os
import urllib.request

from common import *
import archive
import backup

_sheet_url  = "https://docs.google.com/spreadsheets/d/1-eu8GT6_zI4IOTHWFymplV81GJj1Q469FSWv6jGUHH8/export?format=csv&gid=2068465123"
_sheet_path = "data"
_sheet_file = "Frostpunk 翻訳作業所 - 翻訳.csv"

_comn_file  = "common"
_local_file = "localizations"

_lang_path  = "data"
_lang_file  = "lang.csv"

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
        "get sheet path"
        return self.__sheet_file

class Patch():
    "patch japanese translation"

    def __init__(self):
        "constructor"
        path = os.path.join(get_prog_path(), _lang_path)
        path = path.replace("/", os.sep)
        self.__lang_path = path
        path = os.path.join(path, _lang_file)
        self.__lang_file = path

    def patch_font(self):
        "patch font file"
        log("patch font file")
        bk = backup.Backup()
        bpath = bk.backup_path
        path = os.path.join(bpath, _comn_file)
        arc = archive.Archive()
        if not arc.read_archive(path):
            return False
        return True

    def patch_lang(self):
        "patch lang file"
        log("patch lang file")
        return False

    @property
    def lang_exists(self):
        "check exsits lang sheet file"
        return os.path.isfile(self.__lang_file)

    @property
    def lang_path(self):
        "get lang sheet path"
        return self.__lang_file
