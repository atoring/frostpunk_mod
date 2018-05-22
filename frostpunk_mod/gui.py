#!/usr/bin/python
# coding: utf-8

import tkinter as tk
import webbrowser

from common import *
import version

_game_url1  = "http://www.frostpunkgame.com/"
_game_url2  = "https://store.steampowered.com/app/323190/Frostpunk/"
_tool_url1  = "https://github.com/atoring/frostpunk_mod"
_tool_url2  = "https://github.com/atoring/frostpunk_mod/wiki/%E7%B7%8F%E5%90%88MOD%E3%83%84%E3%83%BC%E3%83%AB"
_sheet_url1 = "https://docs.google.com/spreadsheets/d/1-eu8GT6_zI4IOTHWFymplV81GJj1Q469FSWv6jGUHH8/htmlview#"
_sheet_url2 = "https://docs.google.com/spreadsheets/d/1-eu8GT6_zI4IOTHWFymplV81GJj1Q469FSWv6jGUHH8/edit#gid=770455416"

_win_size           = "380x535"
_win_frame_col      = "gray"
_version_fg_col     = "darkblue"
_inf_fg_col         = "darkgreen"
_hover_fg_col       = "blue"
_hover_risk_fg_col  = "red"
_risk_fg_col        = "darkred"
_hover_cur          = "hand2"

class LabelFrame(tk.LabelFrame):
    "label frame"

    def __init__(self, master=None, cnf={}, **kw):
        tk.LabelFrame.__init__(self, master, cnf, **kw)
        self.pack(padx=12, pady=4, ipadx=12, ipady=4, fill=tk.X)

class Frame(tk.Frame):
    "frame"

    def __init__(self, master=None, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)
        self.pack()

class Button(tk.Button):
    "button"

    def __init__(self, master=None, left=False, risk=False, cnf={}, **kw):
        tk.Button.__init__(self, master, cnf, **kw)
        self["relief"]      = tk.FLAT
        self["cursor"]      = _hover_cur
        if risk:
            self.hover_fg_col   = _hover_risk_fg_col
            self.fg_col         = _risk_fg_col
            self["fg"]          = _risk_fg_col
        else:
            self.hover_fg_col   = _hover_fg_col
            self.fg_col         = self["fg"]
        self.bind("<Enter>", lambda event, h=self: h.configure(fg=self.hover_fg_col))
        self.bind("<Leave>", lambda event, h=self: h.configure(fg=self.fg_col))
        if left:
            self.pack(side=tk.LEFT)
        else:
            self.pack()

class LButton(Button):
    "left side button"

    def __init__(self, master=None, risk=False, cnf={}, **kw):
        Button.__init__(self, master, True, risk, cnf, **kw)

class Label(tk.Label):
    "label"

    def __init__(self, master=None, cnf={}, **kw):
        tk.Label.__init__(self, master, cnf, **kw)
        self.pack(side=tk.LEFT)

class Separator(Label):
    "separator label"

    def __init__(self, master=None):
        Label.__init__(self, master, text="/")

class Entry(tk.Label):
    "entry"

    def __init__(self, master=None, cnf={}, **kw):
        tk.Entry.__init__(self, master, cnf, **kw)
        self["relief"]  = tk.FLAT
        self["width"]   = 40
        self.pack(side=tk.LEFT)

class Version(tk.Label):
    "version text"

    def __init__(self, master=None, cnf={}, **kw):
        tk.Label.__init__(self, master, cnf, **kw)
        self["text"]    = "ver %s" % version.version_str
        self["fg"]      = _version_fg_col
        self.pack(padx=12, anchor=tk.E)

class Config():
    "config frame"

    def __init__(self, master=None):
        self.frame              = LabelFrame(master, text="設定")

        self.game_path_frame    = Frame(self.frame)
        self.game_path_label    = Label(self.game_path_frame, text="ゲームパス:")
        self.game_path_entry    = Entry(self.game_path_frame)
        self.open_game_dlg_btn  = LButton(self.game_path_frame, text="...")

        self.game_misc_frame    = Frame(self.frame)
        self.exec_game_btn      = LButton(self.game_misc_frame, text="ゲームを起動")
        self.game_misc_sep      = Separator(self.game_misc_frame)
        self.open_game_exp_btn  = LButton(self.game_misc_frame, text="ゲームフォルダを開く")

    """
    def open_game_dlg(self):

    def exec_game(self):

    def open_game_exp(self):
    """

class ManageData():
    "manage data frame"

    def __init__(self, master=None):
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
        self.frame                  = LabelFrame(master, text="Webサイト")

        self.game_web_frame         = Frame(self.frame)
        self.open_game_web1_btn     = LButton(self.game_web_frame, text="Frostpunkの公式Webサイトを開く", command=self.open_game_web1)
        self.game_web_sep           = Separator(self.game_web_frame)
        self.open_game_web2_btn     = LButton(self.game_web_frame, text="SteamのWebサイトを開く", command=self.open_game_web2)

        self.tool_web_frame         = Frame(self.frame)
        self.open_tool_web1_btn     = LButton(self.tool_web_frame, text="MODツールのWebサイトを開く", command=self.open_tool_web1)
        self.tool_web_sep           = Separator(self.tool_web_frame)
        self.open_tool_web2_btn     = LButton(self.tool_web_frame, text="ヘルプを開く", command=self.open_tool_web2)

        self.sheet_web_frame        = Frame(self.frame)
        self.open_sheet_web1_btn    = LButton(self.sheet_web_frame, text="翻訳シートのWebサイトを開く(閲覧)", command=self.open_sheet_web1)
        self.sheet_web_sep          = Separator(self.sheet_web_frame)
        self.open_sheet_web2_btn    = LButton(self.sheet_web_frame, text="編集で開く", command=self.open_sheet_web2)

    def open_game_web1(self):
        webbrowser.open_new(_game_url1)

    def open_game_web2(self):
        webbrowser.open_new(_game_url2)

    def open_tool_web1(self):
        webbrowser.open_new(_tool_url1)

    def open_tool_web2(self):
        webbrowser.open_new(_tool_url2)

    def open_sheet_web1(self):
        webbrowser.open_new(_sheet_url1)

    def open_sheet_web2(self):
        webbrowser.open_new(_sheet_url2)

class Information(tk.Label):
    "information text"

    def __init__(self, master=None, cnf={}, **kw):
        tk.Label.__init__(self, master, cnf, **kw)
        self["text"]    = "翻訳シート管理人様、翻訳有志諸氏に多大なる感謝を！"
        self["fg"]      = _inf_fg_col
        self.pack()

class Main(tk.Frame):
    "main frame"

    def __init__(self, master=None):
        self.__set_window(master)
        super().__init__(master, highlightthickness=1, highlightbackground=_win_frame_col)
        self.pack(padx=4, pady=4, ipadx=20, ipady=20, fill=tk.BOTH)
        self.__create_widgets()

    def __set_window(self, master=None):
        "setting window"
        master.withdraw()
        master.title("Frostpunk用総合MODツール")
        master.geometry(_win_size)
        master.resizable(0,0)
        self.__center(master)
        master.deiconify()

    def __center(self, master):
        "centering window"
        master.update_idletasks()
        w = master.winfo_screenwidth()
        h = master.winfo_screenheight()
        size = tuple(int(x) for x in master.geometry().split('+')[0].split('x'))
        x = w/2-size[0]/2
        y = h/2-size[1]/2
        master.geometry("%dx%d+%d+%d" % (size+(x,y)))

    def __create_widgets(self):
        "create all widgets"
        self.version        = Version(self)
        self.config         = Config(self)
        self.manage_data    = ManageData(self)
        self.patch          = Patch(self)
        self.link           = Link(self)
        self.inf            = Information(self)

    """
    def on_closing(self):
    """

def main():
    "gui main"
    log("start: gui_main")
    root = tk.Tk()
    main = Main(root)
    main.mainloop()
