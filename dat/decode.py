#!/usr/bin/python
# coding: utf-8

import glob
import gzip
import io
import os
import struct

file_list = {0x781880b4:"english.lang",0xf8b11d94:"french.lang",0x3268a4d1:"german.lang",0x93d6426a:"spanish.lang",0x7d919140:"polish.lang",0xf2232be3:"russian.lang",0xfce49418:"chinese.lang"}

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

def parse_idx(data):
    magic = struct.unpack("<BBB", data[:3])
    print("magic: %02xh,%02xh,%02xh" % magic)
    files,tmp = struct.unpack("<II", data[3:11])
    print("files: %d" % files)
    print("%xh" % tmp)
    idx = []
    for i in range(files):
        id,size1,size2,offset,flag = struct.unpack("<IIIIB", data[11+i*17:28+i*17])
        print("id:%08xh, size1:%08xh, size2:%08xh, offset:%08xh, flag:%02xh" % (id,size1,size2,offset,flag))
        idx.append({"id":id,"size1":size1,"size2":size2,"offset":offset,"flag":flag})
    return idx

def decompress(data):
    # head
    magic = struct.unpack("<BB", data[:2])
#    print("magic: %02xh,%02xh" % magic)
    if magic != (0x1f,0x8b):    # gzip magic
        print("error: magic")
        quit()
    comp = struct.unpack("B", data[2:3])[0]
#    print("comp: %02xh" % comp)
    if comp != 0x08: #  deflate
        print("error: comp")
        quit()
    flag,time,exflag,os = struct.unpack("<BIBB", data[3:10])
#    print("flag: %02xh" % flag)
#    print("time: %08xh" % time)
#    print("exflag: %02xh" % exflag)
#    print("os: %02xh" % os)
    if flag != 0:
        print("error: not supported flag")
        quit()

    # foot
    if False:
        crc,size = struct.unpack("<II", data[len(data)-8:len(data)])
        print("crc: %08xh" % crc)
        print("size: %08xh" % size)

    # decompress
    try:
        bin = gzip.decompress(data)
    except:
        bin = bytearray()
        buf = io.BytesIO()
        buf.write(data)
        buf.seek(0)
        f = gzip.GzipFile(fileobj=buf, mode='rb')
        while True:
            try:
                d = f.read(1)
                if d == "":
                    break
                bin.extend(d)
            except:
                break
        f.close()
    return bin

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

def decode_file(file):
    print("decode: ./data/%s.*" % file)
    idx_path = "./data/%s.idx" % file
    dat_path = "./data/%s.dat" % file
    out_path = "./out/%s" % file

    data = read_bin(idx_path)
    idx = parse_idx(data)
    data = read_bin(dat_path)
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    for i in idx:
        id = i["id"]
        size1 = i["size1"]
        size2 = i["size2"]
        offset = i["offset"]
        flag = i["flag"]

        if id in file_list:
            path = "%s/%s" % (out_path,file_list[id])
        else:
            path = "%s/%08x" % (out_path,id)
        bin = data[offset:offset+size1]
        if flag == 0:
            write_bin(path, bin)
        elif flag == 1:
            dec = decompress(bin)
            dec_size = len(dec)
            print("dec size: %xh" % dec_size)
            if dec_size != size2:
                print("error: size:%xh!=%xh" % (dec_size,size2))
                quit()
            write_bin(path, dec)
        else:
            print("error: flag:%02xh" % flag)
            quit()

def decode():
    path = "./data/*.idx"
    files = glob.glob(path)
    files.sort()
    for f in files:
        decode_file(os.path.splitext(os.path.split(f)[1])[0])

decode()
