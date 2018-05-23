#!/usr/bin/python
# coding: utf-8

import tkinter as tk
from tkinter import filedialog
import configparser
import os
import subprocess
import webbrowser

from common import *
import version

_game_url1  = "http://www.frostpunkgame.com/"
_game_url2  = "https://store.steampowered.com/app/323190/Frostpunk/"
_tool_url1  = "https://github.com/atoring/frostpunk_mod"
_tool_url2  = "https://github.com/atoring/frostpunk_mod/wiki/%E7%B7%8F%E5%90%88MOD%E3%83%84%E3%83%BC%E3%83%AB"
_sheet_url1 = "https://docs.google.com/spreadsheets/d/1-eu8GT6_zI4IOTHWFymplV81GJj1Q469FSWv6jGUHH8/htmlview#"
_sheet_url2 = "https://docs.google.com/spreadsheets/d/1-eu8GT6_zI4IOTHWFymplV81GJj1Q469FSWv6jGUHH8/edit#gid=770455416"

_config_path        = "./config.ini"
_config_code        = "utf-8-sig"
_config_sec         = "config"
_config_game_path   = "game_path"

_def_game_path1     = r"C:\Program Files (x86)\Steam\SteamApps\common\Frostpunk"
_def_game_path2     = r"C:\Program Files\Steam\SteamApps\common\Frostpunk"
_game_exe           = "Frostpunk.exe"

_win_size           = "380x535"
_win_frame_col      = "gray"
_version_fg_col     = "darkblue"
_inf_fg_col         = "darkgreen"
_hover_fg_col       = "blue"
_hover_risk_fg_col  = "red"
_risk_fg_col        = "darkred"
_hover_cur          = "hand2"

def open_dir_exp(path):
    "execute explorer"
    path = correct_path(path)
    if check_path(path):
        subprocess.Popen(["explorer", path])

def exec_path(path, cur_path):
    "execute program"
    path = correct_path(path)
    cur_path = correct_path(cur_path)
    subprocess.Popen([path], cwd=cur_path)

def open_web_site(url):
    "open web site"
    webbrowser.open_new(url)

def correct_path(path):
    "correct path"
    path = os.path.abspath(path)
    path = path.replace("/", os.sep)
    return path

def check_path(path):
    "check path"
    path = correct_path(path)
    return os.path.exists(path)

def check_game_path(path):
    "check path and game exe"
    path = correct_path(path)
    if not os.path.isdir(path):
        return False
    path = os.path.join(path, _game_exe)
    if not os.path.isfile(path):
        return False
    return True

class ConfigFile():
    "config file"

    def __init__(self, path=_config_path, code=_config_code, sec=_config_sec):
        "constructor"
        self.path = path
        self.code = code
        self.sec = sec

    def read(self, key):
        "read data"
        cfg = configparser.ConfigParser()
        cfg.read(self.path, self.code)
        if cfg.has_section(self.sec):
            if cfg.has_option(self.sec, key):
                data = cfg.get(self.sec, key)
                if data:
                    return data
        return None

    def write(self, key, data):
        "write data"
        cfg = configparser.ConfigParser()
        cfg.read(self.path, self.code)
        if not cfg.has_section(self.sec):
            cfg.add_section(self.sec)
        cfg.set(self.sec, key, data)
        cfg.write(open(self.path, "w"))

    def delete(self, key):
        "delete data"
        cfg = configparser.ConfigParser()
        cfg.read(self.path, self.code)
        if cfg.has_section(self.sec):
            if cfg.has_option(self.sec, key):
                cfg.remove_option(self.sec, key)
                cfg.write(open(self.path, "w"))

    @property
    def game_path(self):
        "get game path from config file"
        path = self.read(_config_game_path)
        path_list = [path, _def_game_path1, _def_game_path2]
        for p in path_list:
            p = correct_path(p)
            if check_game_path(p):
                return p
        return None

    @game_path.setter
    def game_path(self, path):
        "set game path to config file"
        path = correct_path(path)
        if check_game_path(path):
            self.write(_config_game_path, path)
        else:
            self.delete(_config_game_path)

class LabelFrame(tk.LabelFrame):
    "label frame"

    def __init__(self, master=None, cnf={}, **kw):
        "constructor"
        super().__init__(master, cnf, **kw)
        self.pack(padx=12, pady=4, ipadx=12, ipady=4, fill=tk.X)

class Frame(tk.Frame):
    "frame"

    def __init__(self, master=None, cnf={}, **kw):
        "constructor"
        super().__init__(master, cnf, **kw)
        self.pack()

class Button(tk.Button):
    "button"

    def __init__(self, master=None, left=False, risk=False, cnf={}, **kw):
        "constructor"
        super().__init__(master, cnf, **kw)
        self["relief"]      = tk.FLAT
        self["cursor"]      = _hover_cur
        if risk:
            self.hover_fg_col   = _hover_risk_fg_col
            self.fg_col         = _risk_fg_col
            self["fg"]          = _risk_fg_col
        else:
            self.hover_fg_col   = _hover_fg_col
            self.fg_col         = self["fg"]
        self.bind("<Enter>", lambda event: self.configure(fg=self.hover_fg_col))
        self.bind("<Leave>", lambda event: self.configure(fg=self.fg_col))
        if left:
            self.pack(side=tk.LEFT)
        else:
            self.pack()

class LButton(Button):
    "left side button"

    def __init__(self, master=None, risk=False, cnf={}, **kw):
        "constructor"
        super().__init__(master, True, risk, cnf, **kw)

class Label(tk.Label):
    "label"

    def __init__(self, master=None, cnf={}, **kw):
        "constructor"
        super().__init__(master, cnf, **kw)
        self.pack(side=tk.LEFT)

class Separator(Label):
    "separator label"

    def __init__(self, master=None):
        "constructor"
        super().__init__(master, text="/")

class Entry(tk.Entry):
    "entry"

    def __init__(self, master=None, text=None, cnf={}, **kw):
        "constructor"
        super().__init__(master, cnf, **kw)
        self["relief"]  = tk.FLAT
        self["width"]   = 40
        if text:
            self.text = text
        self.pack(side=tk.LEFT)

    @property
    def text(self):
        "get text"
        return self.get()

    @text.setter
    def text(self, text):
        "set text"
        self.delete(0, tk.END)
        self.insert(0, text)

class Version(tk.Label):
    "version text"

    def __init__(self, master=None, cnf={}, **kw):
        "constructor"
        super().__init__(master, cnf, **kw)
        self["text"]    = "ver %s" % version.version_str
        self["fg"]      = _version_fg_col
        self.pack(padx=12, anchor=tk.E)

class Config():
    "config frame"

    def __init__(self, master=None):
        "constructor"
        self.frame              = LabelFrame(master, text="設定")

        self.game_path_frame    = Frame(self.frame)
        self.game_path_label    = Label(self.game_path_frame, text="ゲームパス:")
        self.game_path_entry    = Entry(self.game_path_frame, text=master.game_path)
        self.open_game_dlg_btn  = LButton(self.game_path_frame, text="...", command=self.open_game_dlg)

        self.game_misc_frame    = Frame(self.frame)
        self.exec_game_btn      = LButton(self.game_misc_frame, text="ゲームを起動")
        self.game_misc_sep      = Separator(self.game_misc_frame)
        self.open_game_exp_btn  = LButton(self.game_misc_frame, text="ゲームフォルダを開く", command=self.open_game_exp)

    @property
    def game_path(self):
        "get game path from entry"
        path = self.game_path_entry.text
        path = correct_path(path)
        if check_game_path(path):
            return path
        return None

    @game_path.setter
    def game_path(self, path):
        "set game path to entry"
        path = correct_path(path)
        if not check_game_path(path):
            path = ""
        self.game_path_entry.text = path

    def open_game_dlg(self):
        "open directory dialog for game path"
        path = filedialog.askdirectory(initialdir=self.game_path)
        if path:
            self.game_path = path

    def exec_game(self):
        "execute game"
        path = self.game_path
        if path:
            exe_path = os.path.join(path, _game_exe)
            exec_path(exe_path, path)

    def open_game_exp(self):
        "open game path"
        path = self.game_path
        if path:
            open_dir_exp(path)

class ManageData():
    "manage data frame"

    def __init__(self, master=None):
        "constructor"
        self.frame              = LabelFrame(master, text="データ管理")

        self.backup_btn         = Button(self.frame, text="パッチに関係するデータ(4ファイル)をバックアップ")
        self.restore_btn        = Button(self.frame, risk=True, text="パッチに関係するデータ(4ファイル)をリストア")
        self.open_data_exp_btn  = Button(self.frame, text="バックアップデータフォルダを開く")
        self.download_sheet_btn = Button(self.frame, text="翻訳シート(.csv)をWebサイトからダウンロード")
        self.open_sheet_btn     = Button(self.frame, text="ダウンロードした翻訳シート(.csv)を開く")

    """
    def backup_data(self):

    def restore_data(self):

    def open_data_exp(self):

    def download_sheet(self):

    def open_sheet(self):
    """

class Patch():
    "patch frame"

    def __init__(self, master=None):
        "constructor"
        self.frame          = LabelFrame(master, text="パッチ")

        self.patch_font_btn = Button(self.frame, risk=True, text="フォント(binfont)パッチを適応")
        self.patch_lang_btn = Button(self.frame, risk=True, text="翻訳(lang)パッチを適応")
        self.open_lang_btn  = Button(self.frame, text="ゲームの翻訳シート(.csv)を開く")

    """
    def patch_font(self):

    def patch_lang(self):

    def open_lang(self):
    """

class Link():
    "link frame"

    def __init__(self, master=None):
        "constructor"
        self.frame                  = LabelFrame(master, text="Webサイト")

        self.game_web_frame         = Frame(self.frame)
        self.open_game_web1_btn     = LButton(self.game_web_frame, text="Frostpunkの公式Webサイトを開く", command=lambda: open_web_site(_game_url1))
        self.game_web_sep           = Separator(self.game_web_frame)
        self.open_game_web2_btn     = LButton(self.game_web_frame, text="SteamのWebサイトを開く", command=lambda: open_web_site(_game_url2))

        self.tool_web_frame         = Frame(self.frame)
        self.open_tool_web1_btn     = LButton(self.tool_web_frame, text="MODツールのWebサイトを開く", command=lambda: open_web_site(_tool_url1))
        self.tool_web_sep           = Separator(self.tool_web_frame)
        self.open_tool_web2_btn     = LButton(self.tool_web_frame, text="ヘルプを開く", command=lambda: open_web_site(_tool_url2))

        self.sheet_web_frame        = Frame(self.frame)
        self.open_sheet_web1_btn    = LButton(self.sheet_web_frame, text="翻訳シートのWebサイトを開く(閲覧)", command=lambda: open_web_site(_sheet_url1))
        self.sheet_web_sep          = Separator(self.sheet_web_frame)
        self.open_sheet_web2_btn    = LButton(self.sheet_web_frame, text="編集で開く", command=lambda: open_web_site(_sheet_url2))

class Information(tk.Label):
    "information text"

    def __init__(self, master=None, cnf={}, **kw):
        "constructor"
        super().__init__(master, cnf, **kw)
        self["text"]    = "翻訳シート管理人様、翻訳有志諸氏に多大なる感謝を！"
        self["fg"]      = _inf_fg_col
        self.pack()

class Main(tk.Frame):
    "main frame"

    def __init__(self, master=None):
        "constructor"
        self.__set_window(master)
        super().__init__(master, highlightthickness=1, highlightbackground=_win_frame_col)
        self.pack(padx=4, pady=4, ipadx=20, ipady=20, fill=tk.BOTH)
        self.__create_widgets()

    def __set_window(self, master=None):
        "setting window"
        master.withdraw()
        master.title("Frostpunk用総合MODツール")
        master.geometry(_win_size)
        master.resizable(0, 0)
        self.__center(master)
        master.protocol("WM_DELETE_WINDOW", lambda arg=master: self.on_closing(arg))
        master.deiconify()

    def __center(self, master):
        "centering window"
        master.update_idletasks()
        w = master.winfo_screenwidth()
        h = master.winfo_screenheight()
        size = tuple(int(v) for v in master.geometry().split('+')[0].split('x'))
        x = (w - size[0]) // 2
        y = (h - size[1]) // 2
        master.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def __create_widgets(self):
        "create all widgets"
        self.version        = Version(self)
        self.config         = Config(self)
        self.manage_data    = ManageData(self)
        self.patch          = Patch(self)
        self.link           = Link(self)
        self.inf            = Information(self)

    def on_closing(self, master):
        "closing event"
        self.game_path = self.config.game_path
        master.destroy()

    @property
    def game_path(self):
        "get game path from config file"
        cfg = ConfigFile()
        return cfg.game_path

    @game_path.setter
    def game_path(self, path):
        "set game path to config file"
        cfg = ConfigFile()
        cfg.game_path = path

def main():
    "gui main"
    log("start: gui_main")
    root = tk.Tk()
    main = Main(root)
    main.mainloop()
