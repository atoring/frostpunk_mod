#!/usr/bin/python
# coding: utf-8

import codecs
from collections import OrderedDict
import csv
import struct
import time

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

def _null_func(text, ref_text=None):
    "null func"
    return text

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

    def set_all_text(self, text, skip_none=False):
        "set text all lang"
        if skip_none:
            lang_list = self.__text.keys() & lang_indexes
        else:
            lang_list = lang_indexes
        for lang_idx in lang_list:
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

    def read_csv(self, path, fix_func=_null_func, lang_idx=japanese_idx, skip_row=4, csv_column=1):
        "read csv file"
        log("read csv file", path, fix_func, lang_idx, skip_row, csv_column)
        index_list = list(self.__text_list.keys())
        try:
            with codecs.open(path, "r", "utf-8-sig") as f:
                r = csv.reader(f, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
                head = next(r)
#                log("head", head)
                cnt = skip_row
                for data in r:
                    str = data[csv_column]
                    str = fix_func(str)
                    self.__text_list[index_list[cnt]].set_text(lang_idx, str)
                    cnt += 1
        except IOError:
            log("error", "read csv file", path)
            return False
        return True

    def write_csv(self, path, skip_ja=True):
        "write csv file"
        log("write csv file", path, skip_ja)
        if skip_ja:
            lang_list = lang_indexes[:-1]
        else:
            lang_list = lang_indexes
        try:
            with codecs.open(path, "w", "utf-8-sig") as f:
                w = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
                w.writerow(["index"] + lang_list)
                for index, text in self.__text_list.items():
                    data = [index]
                    for lang in lang_list:
                        str = text.get_text(lang)
                        if str is None:
                            str = ""
                        str = str.replace("\n", "</n>") # new line
                        data.append(str)
                    w.writerow(data)
        except IOError:
            log("error", "write csv file", path)
            return False
        log("write len", len(self.__text_list))
        return True

    def set_text(self, lang_idx, index, text):
        "set text"
        log("set text", lang_idx, index, text)
        if index not in self.__text_list:
            return False
        self.__text_list[index].set_text(lang_idx, text)
        return True

    def set_all_text(self, index, text):
        "set text all lang"
        log("set text all lang", index, text)
        if index not in self.__text_list:
            return False
        self.__text_list[index].set_all_text(text)
        return True

    def change_text(self, lang_idx, ref_lang_idx, change_func=_null_func):
        "change text"
        log("change text", lang_idx, ref_lang_idx, change_func)
        cnt = 0
        total = len(self.__text_list)
        step = total/10
        step_cnt = 0
        start = time.time()
        for index, text in self.__text_list.items():
            if False:
                cnt += 1
                step_cnt += 1
                if step_cnt >= step:
                    step_cnt -= step
                    log("processing...", "%d%%" % (100*cnt//total))
            str = text.get_text(lang_idx)
            if str is None:
                str = ""
            ref = text.get_text(ref_lang_idx)
            if ref is None:
                ref = ""
            str = change_func(str, ref)
            text.set_text(lang_idx, str)
        end = time.time()
        log("total: %d sec" % (end - start)
        return True
