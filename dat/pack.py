#!/usr/bin/python
# coding: utf-8

import glob
import gzip
import os
import struct

file_list = {"english.lang":0x781880b4,"french.lang":0xf8b11d94,"german.lang":0x3268a4d1,"spanish.lang":0x93d6426a,"polish.lang":0x7d919140,"russian.lang":0xf2232be3,"chinese.lang":0xfce49418,"notosanscjksc-medium.otf.binfont":0x6b04d7c3}

def read_bin(path):
    print("read file: %s" % path)
    try:
        f = open(path, "rb")
    except IOError:
        print("error: file open error: %s" % path)
        quit()
    data = f.read()
    f.close()
    print("read size: %xh" % len(data))
    return data

def compress(data):
    comp = gzip.compress(data, compresslevel=9)
    return comp

def write_bin(path, data):
    print("write file: %s" % path)
    try:
        f = open(path, "wb")
    except IOError:
        print("error: file open error: %s" % path)
        quit()
    f.write(data)
    f.close()
    print("write size: %xh" % len(data))

def encode_file(file):
    print("encode: ./out/%s/*" % file)
    in_path = "./out/%s/*" % file
    idx_path = "./out/%s.idx" % file
    dat_path = "./out/%s.dat" % file

    files = glob.glob(in_path)
    files.sort()
    idx = bytearray()
    dat = bytearray()
    offset = 0
    idx.extend(struct.pack("<BBBII", 0x00,0x02,0x01,len(files),0))
    for f in files:
        data = read_bin(f)
        comp = compress(data)
        print("comp size: %xh" % len(comp))
        _f = os.path.split(f)[1]
        if _f in file_list:
            id = file_list[_f]
        else:
            id = int(_f, 16)
        size1 = len(comp)
        size2 = len(data)
        flag = 1
        print("id:%08xh, size1:%08xh, size2:%08xh, offset:%08xh, flag:%02xh" % (id,size1,size2,offset,flag))
        idx.extend(struct.pack("<IIIIB", id,size1,size2,offset,flag))
        dat.extend(comp)
        offset += size1

    write_bin(idx_path, idx)
    write_bin(dat_path, dat)

def encode():
    path = "./out/*"
    files = glob.glob(path)
    files.sort()
    for f in files:
        if os.path.isdir(f):
            encode_file(os.path.split(f)[1])

encode()
