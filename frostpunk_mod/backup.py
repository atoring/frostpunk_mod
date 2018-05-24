#!/usr/bin/python
# coding: utf-8

import os

# mod
from common import *

_backup_path = "backup"
_backup_files = [
    "common.idx",
    "common.dat",
    "localizations.idx",
    "localizations.dat",
    ]

class Backup():
    "manage data"

    def __init__(self):
        "constructor"
        path = os.path.join(get_prog_path(), _backup_path)
        path = path.replace("/", os.sep)
        self.__backup_path = path

    def backup(self, path):
        "backup data"
        log("backup", path)
        bpath = self.__backup_path
        if not make_dir(bpath):
            return False
        for file in _backup_files:
            dst = os.path.join(bpath, file)
            src = os.path.join(path, file)
            if not copy_file(dst, src):
                return False
        return True

    def restore(self, path):
        "restore data"
        log("restore", path)
        bpath = self.__backup_path
        if not self.exists:
            log("not exist", bpath)
            return False
        for file in _backup_files:
            dst = os.path.join(path, file)
            src = os.path.join(bpath, file)
            if not copy_file(dst, src):
                return False
        return True

    @property
    def exists(self):
        "check exsits backup data"
        bpath = self.__backup_path
        for file in _backup_files:
            path = os.path.join(bpath, file)
            if not os.path.isfile(path):
                return False
        return True

    @property
    def backup_path(self):
        "get backup path"
        return self.__backup_path
