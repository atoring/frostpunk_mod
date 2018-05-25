#!/usr/bin/python
# coding: utf-8

import os
import re
import urllib.request
import zipfile

# mod
from common import *
import archive
import backup
import language

_sheet_url  = "https://docs.google.com/spreadsheets/d/1-eu8GT6_zI4IOTHWFymplV81GJj1Q469FSWv6jGUHH8/export?format=csv&gid=2068465123"
_sheet_path = "data"
_sheet_file = "Frostpunk 翻訳作業所 - 翻訳.csv"

_cmn_file   = "common"
_loc_file   = "localizations"

_font_path      = "data"
_font_zip_file  = "notosanscjksc-medium.otf.binfont.zip"
_font_gz_file   = "notosanscjksc-medium.otf.binfont.gz"
_font_file      = "notosanscjksc-medium.otf.binfont"
_lang_path      = "data"
_lang_file      = "lang.csv"
_tmp_path       = ".tmp"

_lang_name_zh_index = "UI/Menu/Settings/LanguageNames/Chinese"
_lang_name_ja_text  = "日本語"

def read_zip(path, file):
    "read file in zip file"
    log("read zip file", path, file)
    try:
        with zipfile.ZipFile(path) as zip:
            with zip.open(file, "r") as f:
                data = f.read()
    except:
        log("error", "read zip file", path, file)
        return None
    log("size", "%xh" % len(data))
    return data

def _fix_text(text):
    "fix text"
    text = re.sub("[ 　]+", " ", text)
    text = text.replace("</n>", "\n")   # new line
    for k, v in {"０":"0","１":"1","２":"2","３":"3","４":"4","５":"5","６":"6","７":"7","８":"8","９":"9",",":"、","，":"、","、":"、，","!":"！","?":"？","：":":","／":"/","（":"(","）":")"}.items():
        text = text.replace(k, v)   # replace
    if False:
        for s in ["人","年","月","日","時","分","秒","，","。","！","？","/"]:
            text = re.sub("[ ]*%s[ ]*" % s, s, text)    # reduce length
        for k, v in {r"\(":"(",r"\)":")"}.items():
            text = re.sub("[ ]*%s[ ]*" % k, v, text)    # reduce length
    return text

class Sheet():
    "japanese translation sheet"

    def __init__(self):
        "constructor"
        path = os.path.join(get_prog_path(), _sheet_path)
        path = path.replace("/", os.sep)
        self.__sheet_path = path
        path = os.path.join(path, _sheet_file)
        self.__sheet_file = path

    def fetch(self):
        "fetch sheet from web site"
        log("fetch sheet", _sheet_url)
        try:
            data = urllib.request.urlopen(_sheet_url).read().decode("utf-8")
        except:
            log("error", "fetch sheet", _sheet_url)
            return False
        if not make_dir(self.__sheet_path):
            return False
        return write_txt(self.__sheet_file, data)

    @property
    def exists(self):
        "check exsits sheet file"
        return os.path.isfile(self.__sheet_file)

    @property
    def sheet_path(self):
        "get sheet path"
        return self.__sheet_file

class Patch():
    "patch japanese translation"

    def __init__(self):
        "constructor"
        path = os.path.join(get_prog_path(), _font_path)
        path = path.replace("/", os.sep)
        self.__font_path = path
        path = os.path.join(self.__font_path, _font_zip_file)
        self.__font_zip_file = path
        path = os.path.join(self.__font_path, _font_gz_file)
        self.__font_gz_file = path

        path = os.path.join(get_prog_path(), _lang_path)
        path = path.replace("/", os.sep)
        self.__lang_path = path
        path = os.path.join(path, _lang_file)
        self.__lang_file = path

        path = os.path.join(get_prog_path(), _tmp_path)
        path = path.replace("/", os.sep)
        self.__tmp_path = path

    def patch_font(self, path):
        "patch font file"
        log("patch font file", path)
        if True:
            # read binfont from zip
            font = read_zip(self.__font_zip_file, _font_file)
            if not font:
                return False
        else:
            # read gz binfont
            font = read_bin(self.__font_gz_file)
            if not font:
                return False
        bk = backup.Backup()
        bk_cmn_path = os.path.join(bk.backup_path, _cmn_file)
        tmp_cmn_path = os.path.join(self.__tmp_path, _cmn_file)
        game_cmn_path = os.path.join(path, _cmn_file)
        with archive.Archive() as arc:
            if not arc.read_archive(bk_cmn_path):
                return False
            if True:
                # binfont
                if not arc.set_file(archive.notosans_font_id, font):
                    return False
            else:
                # gz binfont
                if not arc.set_comp_file(archive.notosans_font_id, font):
                    return False
            if not make_dir(self.__tmp_path):
                return False
            if not arc.write_archive(tmp_cmn_path):
                delete_dir(self.__tmp_path)
                return False
        if not self.__copy_archive(game_cmn_path, tmp_cmn_path):
            self.__copy_archive(game_cmn_path, bk_cmn_path)
            delete_dir(self.__tmp_path)
            return False
        delete_dir(self.__tmp_path)
        return True

    def patch_lang(self, path):
        "patch lang file"
        log("patch lang file", path)
        bk = backup.Backup()
        bk_loc_path = os.path.join(bk.backup_path, _loc_file)
        tmp_loc_path = os.path.join(self.__tmp_path, _loc_file)
        game_loc_path = os.path.join(path, _loc_file)
        sheet = Sheet()
        with archive.Archive() as arc:
            if not arc.read_archive(bk_loc_path):
                return False
            lang = language.Language()
            for i in range(len(archive.lang_ids)):
                data = arc.get_file(archive.lang_ids[i])
                if not data:
                    return False
                if not lang.set_data(language.lang_indexes[i], data):
                    return False
            if not lang.write_csv(self.__lang_file):
                return False
            if not lang.read_csv(sheet.sheet_path, _fix_text):
                return False
            # ...
            if not lang.set_all_text(_lang_name_zh_index, _lang_name_ja_text):
                return False
            # ...
            for i in range(len(archive.lang_ids)):
                idx = language.lang_indexes[i]
                if idx == language.chinese_idx:
                    idx = language.japanese_idx
                data = lang.get_data(idx)
                if not data:
                    return False
                if not arc.set_file(archive.lang_ids[i], data):
                    return False
            if not make_dir(self.__tmp_path):
                return False
            if not arc.write_archive(tmp_loc_path):
                delete_dir(self.__tmp_path)
                return False
        if not self.__copy_archive(game_loc_path, tmp_loc_path):
            self.__copy_archive(game_loc_path, bk_loc_path)
            delete_dir(self.__tmp_path)
            return False
        delete_dir(self.__tmp_path)
        return True

    def __copy_archive(self, dst, src):
        "copy archive file"
        log("copy archive file", dst, src)
        if not copy_file(dst + archive.index_ext, src + archive.index_ext):
            return False
        if not copy_file(dst + archive.data_ext, src + archive.data_ext):
            return False
        return True

    @property
    def lang_exists(self):
        "check exsits lang sheet file"
        return os.path.isfile(self.__lang_file)

    @property
    def lang_path(self):
        "get lang sheet path"
        return self.__lang_file
