#!/usr/bin/python
# coding: utf-8

# 翻訳シートをwebから取得して./data/Frostpunk 翻訳作業所 - 翻訳.csvに保存します。
# (手動で取得して保存する事と同等です。)

import urllib.request

url = "https://docs.google.com/spreadsheets/d/1-eu8GT6_zI4IOTHWFymplV81GJj1Q469FSWv6jGUHH8/export?format=csv&gid=2068465123"
path = "./data/Frostpunk 翻訳作業所 - 翻訳.csv"

print("fetch url: %s" % url)
urllib.request.urlretrieve(url, path)
print("write file: %s" % path)
