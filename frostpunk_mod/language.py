#!/usr/bin/python
# coding: utf-8

import struct

# mod
from common import *

english_idx     = 0
french_idx      = 1
german_idx      = 2
spanish_idx     = 3
polish_idx      = 4
russian_idx     = 5
chinese_idx     = 6
japanese_idx    = 7

class Text():
    "text"

    def __init__(self):
        "constructor"
        self.__text = None

    @property
    def text(self):
        "get text"
        return self.__text

    @text.setter
    def text(self, text):
        "set text"
        self.__text = text

class Language():
    "language"

    def __init__(self):
        "constructor"
        self.__text_list = {}

    def read_file(self, lang_idx, path):
        "read lang file"
        log("read lang file", lang_idx, path)
        data = read_bin(path)
        if data:
            if not self.read_data(lang_idx, data):
                return False
        return True

    def read_data(self, lang_idx, data):
        "read lang data"
        log("read lang data", lang_idx, len(data))
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
                self.__text_list[index].text[lang_idx] = str
            else:
                text = Text()
                text.text = {lang_idx:str}
                self.__text_list[index] = text
            cnt += 1
        return True

    def write_file(self, lang_idx, path):
        "write lang file"
        log("write lang file", lang_idx, path)

    def write_data(self, lang_idx):
        "write lang data"
        log("write lang data", lang_idx)
