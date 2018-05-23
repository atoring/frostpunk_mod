#!/usr/bin/python
# coding: utf-8

import os
import shutil

from common import *

_backup_path = "./backup"
_backup_files = [
    "common.idx",
    "common.dat",
    "localizations.idx",
    "localizations.dat",
    ]

def make_dir(path):
    "make dir"
    log("make dir", path)
    if os.path.exists(path):
        log("already exist", path)
        return True
    try:
        os.mkdir(path)
    except:
        log("error", "make_dir", path)
        return False
    return True

def copy_file(dst, src):
    "copy file"
    log("copy file", dst, src)
    if not os.path.exists(src):
        log("not exist", src)
        return False
    if os.path.exists(dst):
        log("overwrite file", dst)
    try:
        shutil.copy2(src, dst)
    except:
        log("error", "copy_file", dst, src)
        return False
    return True

class Backup():
    "manage data"

    def backup(self, path):
        "backup data"
        log("backup", path)
        bpath = self.backup_path
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
        bpath = self.backup_path
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
        bpath = self.backup_path
        for file in _backup_files:
            path = os.path.join(bpath, file)
            if not os.path.isfile(path):
                return False
        return True

    @property
    def backup_path(self):
        "get backup path"
        path = _backup_path
        path = os.path.abspath(path)
        path = path.replace("/", os.sep)
        return path
