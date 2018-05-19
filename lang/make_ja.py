#!/usr/bin/python
# coding: utf-8

# ./out/lang.csvと./data/Frostpunk 翻訳作業所 - 翻訳.csvから./out/japanese_*.langを生成します。
# (翻訳シートの構成が変わった場合は使用できません。)

import codecs
import csv
import re
import struct
from janome.tokenizer import Tokenizer  # see: http://mocobeta.github.io/janome/

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
            if False:
                if d[i] != "":
                    strs[i-1][s] = d[i]
            else:
                strs[i-1][s] = d[i]
    return strs

def marge_data(data1, data2, skip, index1, index2):
    strs = {}
    cnt = 0
    for d in data1.keys():
        if skip > 0:
            skip -= 1
            continue
        if cnt >= len(data2):
            break
        if data2[cnt][index1] != "":
            strs[d] = data2[cnt][index1]
        elif "{" not in data1[d] and index2>=0 and data2[cnt][index2]!="":
            strs[d] = data2[cnt][index2]
        else:
            strs[d] = data1[d]
        cnt += 1
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
    for d in data.keys():
        f.write("%s\n" % d)
        f.write("%s\n" % data[d])
    f.close()
    print("write len: %d" % len(data))

def make_lang(data):
    bin = bytearray()
    bin.extend(struct.pack("<II", 0, len(data)))
    for d in data.keys():
        if True:    # fix
            if d == "UI/Menu/Settings/LanguageNames/Chinese":
                data[d] = "日本語"
        bin.extend(struct.pack("<H", len(d)))
        bin.extend(d.encode("ascii"))
        _d = data[d]
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

def get_macros(data):
    macros = set()
    for d in data.values():
        macros.update(set(re.findall(r"({.*?}|\|.*?\|)", d)))
    macros = set(sorted(macros))
#    print(macros)
    return macros

def check_macros(macros1, macros2, data):
    diff = macros2.difference(macros1)
#    print(diff)
    if len(diff) > 0:
        fnd = False
        cnt = 2
        for d in data.values():
            if cnt != 2237:
                m = set(re.findall(r"({.*?}|\|.*?\|)", d))
                if len(m) > 0:
                    _m = diff.intersection(m)
                    if len(_m) > 0:
                        print("error: line=",cnt,", macro=",_m)
                        fnd = True
            cnt += 1
        if fnd:
            print("### 翻訳シートにマクロエラーがありました。翻訳シートを修正してください。 ###")
            input("何かキーを入力してください。")

def check_exmacros(data):
    fnd = False
    cnt = 2
    for d in data.values():
        if cnt != 270:
            if re.search("<", d):
                print("error: line=",cnt,", ",d)
                fnd = True
        cnt += 1
    if fnd:
        print("### 翻訳シートに拡張マクロエラーがありました。翻訳シートを修正してください。 ###")
        input("何かキーを入力してください。")

def fix_data(data):
    for d in data.keys():
        _d = data[d]
        _d = re.sub("[ 　]+", " ", _d)
        _d = re.sub(r"<[/\][ ]*[nN]>", "\n", _d)    # new line
        for k,v in {"０":"0","１":"1","２":"2","３":"3","４":"4","５":"5","６":"6","７":"7","８":"8","９":"9",",":"、","，":"、","、":"、，","!":"！","?":"？","：":":","／":"/","（":"(","）":")"}.items():
            _d = _d.replace(k, v)   # replace
        if False:
            for s in ["人","年","月","日","時","分","秒","，","。","！","？","/"]:
                _d = re.sub("[ ]*%s[ ]*" % s, s, _d)    # reduce length
            for k,v in {r"\(":"(",r"\)":")"}.items():
                _d = re.sub("[ ]*%s[ ]*" % k, v, _d)    # reduce length
        data[d] = _d
    return data

def get_max_sentence_len(str):
    str = re.sub("<.*?>", "\n", str)
    str = re.sub(r"\|.*?\|", "", str)
    str = re.sub("{.*?}", "00000", str)
    s = re.split("[\n，。！？]", str)
#    print(s)
    l = [len(_s) for _s in s]
    max = sorted(set(l), reverse=True)[0]
    return max

def insert_comma(data1, data2):
    print("日本語を解析して処理しています...")
    t = Tokenizer()
    cnt = 0
    total = len(data1)
    step = total/10
    step_cnt = 0
    for d in data1.keys():
        d1 = data1[d]
        l1 = get_max_sentence_len(d1)
        d2 = data2[d]
        l2 = get_max_sentence_len(d2)
        cnt += 1
        step_cnt += 1
        if step_cnt >= step:
            step_cnt -= step
            print("%d%%" % (100*cnt//total))
        if l1>4 and l1>l2:
            try:
                re.sub("[！？]", "", d1).encode("ascii")
            except:
                tokens = t.tokenize(d1)
                str = ""
                jf = False
                for token in tokens:
                    pos = token.part_of_speech.split(',')
                    if jf:
                        if pos[0]!="助詞" and pos[1]!="読点" and pos[1]!="句点":
                            str += "，"
                        jf = False
                    if pos[1]=="係助詞" or pos[1]=="格助詞":
                        jf = True
                    str += token.surface
                data1[d] = str
    return data1

def make_ja():
    data = read_csv("./out/lang.csv")
    if False:
        en,fr,de,es,pl,ru,zh = split_data(data)
    else:
        en,zh,fr,de,es,pl,ru = split_data(data)
    macros = get_macros(en)

    data2 = read_csv("./data/Frostpunk 翻訳作業所 - 翻訳.csv")

    # uninclude Machine Translation
    ja = marge_data(en, data2, 4, 1, -1)
    ja = fix_data(ja)
    ja = insert_comma(ja, zh)
    check_macros(macros, get_macros(ja), ja)
    check_exmacros(ja)
#    write_txt("./out/japanese.txt", ja)
    write_bin("./out/japanese.lang", make_lang(ja))

    # include Machine Translation
    ja = marge_data(en, data2, 4, 1, 2)
    ja = fix_data(ja)
    ja = insert_comma(ja, zh)
#    check_macros(macros, get_macros(ja), ja)
#    check_exmacros(ja)
#    write_txt("./out/japanese_wmt.txt", ja)
    write_bin("./out/japanese_wmt.lang", make_lang(ja))

    if True:
        write_bin("./out/english.lang", make_lang(en))
        write_bin("./out/french.lang", make_lang(fr))
        write_bin("./out/german.lang", make_lang(de))
        write_bin("./out/spanish.lang", make_lang(es))
        pl = make_lang(pl)
        write_bin("./out/polish.lang", pl)
#        write_bin("./out/7D919140.dat", pl)
        write_bin("./out/russian.lang", make_lang(ru))
        write_bin("./out/chinese.lang", make_lang(zh))

make_ja()
