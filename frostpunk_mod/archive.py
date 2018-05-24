#!/usr/bin/python
# coding: utf-8

import gzip
import io
import struct

from common import *

font_index  = 0x6b04d7c3

_index_ext  = ".idx"
_data_ext   = ".dat"

_idx_id             = "id"
_idx_data_size      = "data_size"
_idx_decode_size    = "decode_size"
_idx_offset         = "offset"
_idx_flag           = "flag"

_comp_level = 6
#_comp_level = 9

def decompress(data, dec_size=None):
    "decompress data"
    log("decompress data", len(data), dec_size)

    # head
    offset = 0
    magic = struct.unpack_from("<BB", data, offset)
    offset += 2
#    log("magic", magic)
    if magic != (0x1f, 0x8b):   # gzip magic
        log("error", "magic")
        return None
    comp = struct.unpack_from("B", data, offset)[0]
    offset += 1
#    log("comp", comp)
    if comp != 0x08:    # deflate
        log("error", "comp")
        return None
    flag, time, exflag, os = struct.unpack_from("<BIBB", data, offset)
    offset += 7
#    log("flag", flag)
#    log("time", time)
#    log("exflag", exflag)
#    log("os", os)
    if flag != 0:
        log("error", "flag")
        return None

    # foot
    if False:
        crc, size = struct.unpack_from("<II", data, -8)
        log("crc", crc)
        log("size", size)

    # decompress
    try:
        dec_data = gzip.decompress(data)
    except:
        if dec_size is None:
            return None
        buf = io.BytesIO()
        buf.write(data)
        buf.seek(0)
        with gzip.GzipFile(fileobj=buf, mode="rb") as f:
            dec_data = f.read(dec_size)
    log("dec size", len(dec_data))
    if dec_size is not None and len(dec_data) != dec_size:
        log("error", "dec size")
        return None
    return dec_data

def compress(data, compresslevel=_comp_level):
    "compress data"
    log("compress data", len(data), compresslevel)
    comp_data = gzip.compress(data, compresslevel)
    log("comp size", len(comp_data))
    return comp_data

class File():
    "file"

    def __init__(self, master):
        "constructor"
        self.__master       = master
        self.__index        = {}
        self.__data         = None
        self.__comp_data    = None

    @property
    def index(self):
        "get index"
        return self.__index

    @index.setter
    def index(self, index):
        "set index"
        self.__index = index

    @property
    def data(self):
        "get data"
        if not self.__data:
            data = self.comp_data
            if data:
                if self.__index[_idx_flag] == 0:
                    self.__data = data
                else:
                    size        = self.__index[_idx_decode_size]
                    self.__data = decompress(data, size)
        return self.__data

    @data.setter
    def data(self, data):
        "set data"
        self.__data                     = data
        self.__index[_idx_decode_size]  = len(data)

        self.__comp_data                = compress(data)
        self.__index[_idx_data_size]    = len(self.__comp_data)

        self.__index[_idx_offset]       = None
        self.__index[_idx_flag]         = 1

    @property
    def comp_data(self):
        "get compression data"
        if not self.__comp_data:
            offset  = self.__index[_idx_offset]
            size    = self.__index[_idx_data_size]
            if offset is not None and size is not None:
                self.__comp_data = self.__master._get_data(offset, size)
        return self.__comp_data

    @comp_data.setter
    def comp_data(self, data):
        "set compression data"
        self.__comp_data                = data
        self.__index[_idx_data_size]    = len(data)

        self.__data                     = decompress(data)
        self.__index[_idx_decode_size]  = len(self.__data)

        self.__index[_idx_offset]       = None
        self.__index[_idx_flag]         = 1

    def reduction_data(self):
        "reduction memory"
        if self.__index[_idx_offset] is not None:
            self.__data         = None
            self.__comp_data    = None

class Archive():
    "idx+dat archive"

    def __init__(self):
        "constructor"
        self.__path         = None
        self.__index_path   = None
        self.__data_path    = None
        self.__file_list    = {}
        self.__data         = None

    def __enter__(self):
        "enter"
        return self

    def __exit__(self, *exc):
        "exit"
        self.close()

    def read_archive(self, path):
        "open idx file"
        log("read archive", path)
        self.close()
        self.__path         = path
        self.__index_path   = path + _index_ext
        self.__data_path    = path + _data_ext
        if not self.__parse_index():
            return False
        return True

    def __parse_index(self):
        "parse idx file"
        log("parse idx file", self.__index_path)
        self.__file_list = {}
        data = read_bin(self.__index_path)
        if not data:
            return False
        offset = 0
        magic = struct.unpack_from("<BBB", data, offset)
        offset += 3
        log("magic", magic)
        files, tmp = struct.unpack_from("<II", data, offset)
        offset += 8
        log("files", files)
        log("tmp", tmp)
        cnt = 0
        size = len(data)
        index_struct = struct.Struct("<IIIIB")
        while cnt < files and offset + 17 <= size:
            idx_id, idx_data_size, idx_decode_size, idx_offset, idx_flag = index_struct.unpack_from(data, offset)
            offset += 17
            index = {_idx_id:idx_id, _idx_data_size:idx_data_size, _idx_decode_size:idx_decode_size, _idx_offset:idx_offset, _idx_flag:idx_flag}
#            log("index", index)
            file = File(self)
            file.index = index
            self.__file_list[idx_id] = file
            cnt += 1
        return True

    def write_archive(self, path):
        "write idx+dat archive"
        log("write archive", path)
        if path == self.__path:
            return False
        index_path  = path + _index_ext
        data_path   = path + _data_ext
        file_list = sorted(self.__file_list.items())
        log("open file", data_path)
        with open(data_path, "wb") as fd:
            log("open file", index_path)
            with open(index_path, "wb") as fi:
                fi.write(struct.pack("<BBBII", 0x00, 0x02, 0x01, len(file_list), 0))    # head
                index_struct = struct.Struct("<IIIIB")
                offset = 0
                for id, file in file_list:
                    data = file.comp_data
                    file.reduction_data()
                    fd.write(data)
                    index = file.index
                    fi.write(index_struct.pack(index[_idx_id], index[_idx_data_size], index[_idx_decode_size], offset, index[_idx_flag]))
                    offset += len(data)
            log("close file", index_path)
        log("close file", data_path)
        return True

    def close(self):
        "all close"
        log("close")
        if self.__data:
            log("close file", self.__data_path)
            self.__data.close()
            self.__data     = None
        self.__file_list    = {}
        self.__path         = None
        self.__index_path   = None
        self.__data_path    = None

    def get_file(self, id):
        "get file from archive"
        log("get file", id)
        file = self.__file_list[id]
        if file:
            data = file.data
            log("size", len(data))
            return data
        return None

    def set_file(self, id, data):
        "set file to archive"
        log("set file", id, len(data))
        file = self.__file_list[id]
        if file:
            file.data = data
            return True
        return False

    def _get_data(self, offset, size):
        "get data from dat file"
#        log("get data", offset, size)
        if not self.__data:
            if not self.__data_path:
                return None
            try:
                log("open file", self.__data_path)
                self.__data = open(self.__data_path, "rb")
            except:
                return None
        try:
            self.__data.seek(offset)
            data = self.__data.read(size)
        except:
            return None
        return data
