#!/usr/bin/python
# coding: utf-8

import codecs
from collections import OrderedDict
import csv
import struct

# mod
from common import *

english_idx     = "english"
french_idx      = "french"
german_idx      = "german"
spanish_idx     = "spanish"
polish_idx      = "polish"
russian_idx     = "russian"
chinese_idx     = "chinese"
japanese_idx    = "japanese"
id_text_idx     = "id_text"
lang_indexes = [
    english_idx,
    french_idx,
    german_idx,
    spanish_idx,
    polish_idx,
    russian_idx,
    chinese_idx,
    japanese_idx,
    ]

class Text():
    "text"

    def __init__(self, index=None):
        "constructor"
        self.__text = {}
        self.index = index

    @property
    def index(self):
        "get index text"
        return self.get_text(id_text_idx)

    @index.setter
    def index(self, text):
        "set index text"
        self.set_text(id_text_idx, text)

    def get_text(self, lang_idx):
        "get text"
        if lang_idx in self.__text:
            return self.__text[lang_idx]
        return None

    def set_text(self, lang_idx, text):
        "set text"
        self.__text[lang_idx] = text

class Language():
    "language"

    def __init__(self):
        "constructor"
        self.__text_list = OrderedDict()

    def read_file(self, lang_idx, path):
        "read lang file"
        log("read lang file", lang_idx, path)
        data = read_bin(path)
        if data:
            if self.set_data(lang_idx, data):
                return True
        return False

    def set_data(self, lang_idx, data):
        "set lang data"
        log("set lang data", lang_idx, len(data))
        offset = 0
        size, texts = struct.unpack_from("<II", data, offset)
        offset += 8
        log("size", size)
        log("texts", texts)
        cnt = 0
        size_struct = struct.Struct("<H")
        while cnt < texts and offset < size:
            text_size = size_struct.unpack_from(data, offset)[0]
            offset += 2
#            log("text size", text_size)
            index = data[offset:offset+text_size].decode("ascii")
            offset += text_size
#            log("index", index)
            text_size = size_struct.unpack_from(data, offset)[0]*2
            offset += 2
#            log("text size", text_size)
            str = data[offset:offset+text_size].decode("utf-16-le")
            offset += text_size
#            log("str", str)
            if index in self.__text_list:
                text = self.__text_list[index]
            else:
                text = Text(index)
                self.__text_list[index] = text
            text.set_text(lang_idx, str)
            cnt += 1
        return True

    def write_file(self, lang_idx, path):
        "write lang file"
        log("write lang file", lang_idx, path)
        data = self.get_data(lang_idx)
        if data:
            if write_bin(path, data):
                return True
        return False

    def get_data(self, lang_idx):
        "get lang data"
        log("get lang data", lang_idx)
        head_struct = struct.Struct("<II")
        size_struct = struct.Struct("<H")
        data = bytearray()
        data.extend(head_struct.pack(0, 0))
        cnt = 0
        for index, text in self.__text_list.items():
            str = text.get_text(lang_idx)
            if str is not None:
                data.extend(size_struct.pack(len(index)))
                data.extend(index.encode("ascii"))
                data.extend(size_struct.pack(len(str)))
                data.extend(str.encode("utf-16-le"))
                cnt += 1
        data[:8] = head_struct.pack(len(data) - 4, cnt)
        return data

    def write_csv(self, path):
        "write csv file"
        log("write csv file", path)
        try:
            with codecs.open(path, "w", "utf-8-sig") as f:
                w = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
                w.writerow(["index"] + lang_indexes[:-1])
                for index, text in self.__text_list.items():
                    data = [index]
                    for lang in lang_indexes[:-1]:
                        str = text.get_text(lang)
                        if str is None:
                            str = ""
                        str = str.replace("\n", "</n>")
                        data.append(str)
                    w.writerow(data)
        except IOError:
            log("error", "write csv file", path)
            return False
        log("write len", len(self.__text_list))
        return True
