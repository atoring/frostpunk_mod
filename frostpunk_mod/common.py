#!/usr/bin/python
# coding: utf-8

import codecs
import datetime
#import logging
import os
from pprint import pprint
import shutil
import sys

__prog_path     = None
__log_func      = None
__log_verbose   = False
__def_code      = "utf-8-sig"

def set_log_func(func):
    "set function of output log"
    global __log_func
    __log_func = func

def log(*args):
    "output to log"
    if __log_func:
        __log_func(args)
    else:
        now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        print(now)
        pprint(args)
        if __log_verbose:
            func = sys._getframe(1).f_locals
            pprint(func)

def get_prog_path():
    "get path of running script"
    global __prog_path
    if not __prog_path:
        path = os.path.abspath(sys.argv[0])
        path = os.path.dirname(path)
        path = path.replace("/", os.sep)
        __prog_path = path
    return __prog_path

def read_bin(path):
    "read binary data from file"
    log("read binary file", path)
    try:
        with open(path, "rb") as f:
            data = f.read()
    except IOError:
        log("error", "read binary file", path)
        return None
    log("read binary size", "%xh" % len(data))
    return data

def read_txt(path, code=__def_code):
    "read text data from file"
    log("read text file", path)
    try:
        with codecs.open(path, "r", code) as f:
            data = f.readlines()
    except IOError:
        log("error", "read text file", path)
        return None
    log("read text lines", "%d" % len(data))
    return data

def write_bin(path, data):
    "write binary data to file"
    log("write binary file", path)
    try:
        with open(path, "wb") as f:
            f.write(data)
    except IOError:
        log("error", "write binary file", path)
        return False
    log("write binary size", "%xh" % len(data))
    return True

def write_txt(path, data, code=__def_code):
    "write text data to file"
    log("write text file", path)
    try:
        with codecs.open(path, "w", code) as f:
            f.write(data)
    except IOError:
        log("error", "write text file", path)
        return False
    if isinstance(data, str) or isinstance(data, bytes):
        log("write text size", "%xh" % len(data))
    else:
        log("write text lines", "%d" % len(data))
    return True

def make_dir(path):
    "make directory"
    log("make dir", path)
    if os.path.exists(path):
        log("already exist", path)
        return True
    try:
        os.mkdir(path)
    except:
        log("error", "make dir", path)
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
        log("error", "copy file", dst, src)
        return False
    return True
