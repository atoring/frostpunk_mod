#!/usr/bin/python
# coding: utf-8

# ./out/lang.csvから./out/*.langを生成します。(確認用)

import codecs
import csv
import struct

def read_csv(path):
    print("read file: %s" % path)
    try:
        f = codecs.open(path, "r", "utf_8_sig") # with bom
    except IOError:
        print("error: file open error: %s" % path)
        quit()
    r = csv.reader(f, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    head = next(r)
    data = []
    for d in r:
        data.append(d)
    f.close()
    print("read len: %d" % len(data))
    return data

def split_data(data):
    strs = []
    for i in range(1,len(data[0])):
        strs.append({})
    for d in data:
        s = d[0]
        for i in range(1,len(d)):
            if d[i] != "":
                strs[i-1][s] = d[i]
    return strs

def make_lang(data):
    bin = bytearray()
    bin.extend(struct.pack("<II", 0, len(data)))
    for d in data.keys():
        bin.extend(struct.pack("<H", len(d)))
        bin.extend(d.encode("ascii"))
        _d = data[d].replace("</n>", "\n") # for Frostpunk LANG Tool
        bin.extend(struct.pack("<H", len(_d)))
        bin.extend(_d.encode("utf_16_le"))
    bin[:4] = struct.pack("<I", len(bin)-4)
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

def csv2lang():
    data = read_csv("./out/lang.csv")
    if False:
        en,fr,de,es,pl,ru,zh = split_data(data)
    else:
        en,zh,fr,de,es,pl,ru = split_data(data)
    write_bin("./out/english.lang", make_lang(en))
    write_bin("./out/french.lang", make_lang(fr))
    write_bin("./out/german.lang", make_lang(de))
    write_bin("./out/spanish.lang", make_lang(es))
    write_bin("./out/7D919140.lang", make_lang(pl)) # polish
    write_bin("./out/russian.lang", make_lang(ru))
    write_bin("./out/chinese.lang", make_lang(zh))

csv2lang()
