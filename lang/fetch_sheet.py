#!/usr/bin/python
# coding: utf-8

# 翻訳シートをwebから取得して./data/Frostpunk 翻訳作業所 - 翻訳.csvに保存します。
# (手動で取得して保存する事と同等です。)

import codecs
import urllib.request

def write_txt(path, data):
    print("write file: %s" % path)
    try:
        f = codecs.open(path, "w", "utf_8_sig") # with bom
    except IOError:
        print("error: file open error: %s" % path)
        quit()
    f.write(data)
    f.close()
    print("write size: %xh" % len(data))

def fetch_sheet():
    url = "https://docs.google.com/spreadsheets/d/1-eu8GT6_zI4IOTHWFymplV81GJj1Q469FSWv6jGUHH8/export?format=csv&gid=2068465123"
    path = "./data/Frostpunk 翻訳作業所 - 翻訳.csv"

    print("fetch url: %s" % url)
    data = urllib.request.urlopen(url).read().decode("utf_8")
    write_txt(path, data)

fetch_sheet()
