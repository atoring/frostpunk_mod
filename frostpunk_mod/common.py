#!/usr/bin/python
# coding: utf-8

import codecs
import datetime
#import logging
import sys

__log_func = None
__def_code = "utf-8-sig"

def set_log_func(func):
    "set function of output log"
    global __log_func
    __log_func = func

def log(*args):
    "output to log"
    if __log_func:
        __log_func(args)
    else:
        now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S |")
        func = sys._getframe(1).f_locals
        print(now, args)
        print(func)

def read_bin(path):
    "read binary data from file"
    log("read file: %s" % path)
    try:
        f = open(path, "rb")
    except IOError:
        log("error: file open error: %s" % path)
        quit()
    data = f.read()
    f.close()
    log("read size: %xh" % len(data))
    return data

def read_txt(path, code=__def_code):
    "read text data from file"
    log("read file: %s" % path)
    try:
        f = codecs.open(path, "r", code)
    except IOError:
        log("error: file open error: %s" % path)
        quit()
    data = f.readlines()
    f.close()
    log("read lines: %d" % len(data))
    return data

def write_bin(path, data):
    "write binary data to file"
    log("write file: %s" % path)
    try:
        f = open(path, "wb")
    except IOError:
        log("error: file open error: %s" % path)
        quit()
    f.write(data)
    f.close()
    log("write size: %xh" % len(data))

def write_txt(path, data, code=__def_code):
    "write text data to file"
    log("write file: %s" % path)
    try:
        f = codecs.open(path, "w", code)
    except IOError:
        log("error: file open error: %s" % path)
        quit()
    f.write(data)
    f.close()
    log("write len: %d" % len(data))
