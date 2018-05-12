#!/usr/bin/python
# coding: utf-8

# ./data/*.langから./out/lang.csvを生成します。(全言語の対比表)

import codecs
import csv
import os
import struct

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

def read_lang(path):
    bin = read_bin(path)
    size,count = struct.unpack("<II", bin[:4*2])
    print("data size: %xh" % size)
    print("data count: %d" % count)
    offset = 4*2
    strs = {}
    for i in range(count):
        len = struct.unpack("<H", bin[offset:offset+2])[0]
        offset += 2
        str1 = bin[offset:offset+len].decode("ascii")
        offset += len
        len = struct.unpack("<H", bin[offset:offset+2])[0]*2
        offset += 2
        str2 = bin[offset:offset+len].decode("utf_16_le")
        offset += len
        strs[str1] = str2
    return strs

# for test
# Frostpunk LANG Tool incompatible
def write_txt(path, data):
    print("write file: %s" % path)
    try:
        f = codecs.open(path, "w", "utf_8_sig") # with bom
    except IOError:
        print("error: file open error: %s" % path)
        quit()
    for d in data.values():
        d = d.replace("\n", "</n>") # for Frostpunk LANG Tool
        f.write("%s\n" % d)
    f.close()
    print("write len: %d" % len(data))

def marge_data(data):
    strs = {}
    str = []
    for d in data:
        str.extend(d.keys())
#    str = sorted(set(str))
    str = sorted(set(str), key=str.index)
    for s in str:
        strs[s] = []
        for d in data:
            if s in d.keys():
                strs[s].append(d[s])
            else:
                strs[s].append("")
    return strs

def write_csv(path, head, data):
    print("write file: %s" % path)
    try:
        f = codecs.open(path, "w", "utf_8_sig") # with bom
    except IOError:
        print("error: file open error: %s" % path)
        quit()
    w = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
    w.writerow(head)
    for d in data.keys():
        str = [d]
        for _d in data[d]:
            _d = _d.replace("\n", "</n>") # for Frostpunk LANG Tool
            str.append(_d)
        w.writerow(str)
    f.close()
    print("write len: %d" % len(data))

def lang2csv():
    en = read_lang("./data/english.lang")
#    write_txt("./out/english.txt", en)
    fr = read_lang("./data/french.lang")
#    write_txt("./out/french.txt", fr)
    de = read_lang("./data/german.lang")
#    write_txt("./out/german.txt", de)
    es = read_lang("./data/spanish.lang")
#    write_txt("./out/spanish.txt", es)
    if os.path.exists("./data/polish.lang"):
        pl = read_lang("./data/polish.lang")
    elif os.path.exists("./data/7D919140.dat"):
        pl = read_lang("./data/7D919140.dat")
    else:
        print("error: file not exist:./data/polish.lang or ./data/7D919140.dat")
        quit()
#    write_txt("./out/7D919140.txt", pl)
    ru = read_lang("./data/russian.lang")
#    write_txt("./out/russian.txt", ru)
    zh = read_lang("./data/chinese.lang")
#    write_txt("./out/chinese.txt", zh)
    if False:
        data = marge_data([en,fr,de,es,pl,ru,zh])
        write_csv("./out/lang.csv", ["ID","英語","フランス語","ドイツ語","スペイン語","ポーランド語","ロシア語","中国語(簡体字)"], data)
    else:
        data = marge_data([en,zh,fr,de,es,pl,ru])
        write_csv("./out/lang.csv", ["ID","英語","中国語(簡体字)","フランス語","ドイツ語","スペイン語","ポーランド語","ロシア語"], data)

lang2csv()
