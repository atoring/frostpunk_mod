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
__log_verbose   = False
__log_path      = "log.txt"
__log_file      = None
__def_code      = "utf-8-sig"

def __write_log_file(*args):
    "write log to file"
    global __log_file
    if __log_file is None:
        path = os.path.join(get_prog_path(), __log_path)
        __log_file = codecs.open(path, "a", __def_code)
        print("\n----------------------------------------------------------------------------------------------------", file=__log_file)
    if __log_file is not None:
        now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        print(now, file=__log_file)
        pprint(args, stream=__log_file)
        if __log_verbose:
            func = sys._getframe(1).f_locals
            pprint(func, stream=__log_file)

def __close_log_file():
    "close log file"
    global __log_file
    if __log_file is not None:
        print("----------------------------------------------------------------------------------------------------\n", file=__log_file)
        __log_file.close()
        __log_file = None

__log_func          = __write_log_file
__close_log_func    = __close_log_file

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

def close_log():
    "close log"
    if __close_log_func:
        __close_log_func()

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
    log("read text lines", len(data))
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
        log("write text lines", len(data))
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

def delete_dir(path):
    "delete directory"
    log("delete dir", path)
    if not os.path.exists(path):
        log("not exist", path)
        return True
    try:
#        os.rmdir(path)
        shutil.rmtree(path)
    except:
        log("error", "delete dir", path)
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
