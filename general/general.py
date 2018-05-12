#!/usr/bin/python
# coding: utf-8

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import configparser
import os
import shutil
import subprocess
import webbrowser

version = "20180513"
game_url = "https://store.steampowered.com/app/323190/Frostpunk/"
tool_url = "https://github.com/atoring/frostpunk_mod"
sheet_url = "https://docs.google.com/spreadsheets/d/1-eu8GT6_zI4IOTHWFymplV81GJj1Q469FSWv6jGUHH8"
def_app_path1 = "C:/Program Files (x86)/Steam/SteamApps/common/Frostpunk"
def_app_path2 = "C:/Program Files/Steam/SteamApps/common/Frostpunk"
game_path = ""

def read_config():
    global game_path
    cfg = configparser.ConfigParser()
    cfg.read("./general.conf")
    if cfg.has_section("config"):
        path = cfg.get("config", "game_path")
        if path != None:
            game_path = path

def write_config():
    cfg = configparser.ConfigParser()
    cfg.read('./general.conf', "utf_8")
    if not cfg.has_section("config"):
        cfg.add_section("config")
    cfg.set("config", "game_path", game_path)
    cfg.write(open("./general.conf", "w"))

def open_dir(path):
    if path=="" or not os.path.exists(path) or not os.path.isdir(path):
        messagebox.showerror("エラー", 'フォルダ"%s"がありません。' % path)
        return

    subprocess.Popen(["explorer", os.path.abspath(path)])

def open_csv(path):
    if path=="" or not os.path.exists(path) or not os.path.isfile(path):
        messagebox.showerror("エラー", 'ファイル"%s"がありません。' % path)
        return

    subprocess.Popen(["start", "", os.path.abspath(path)], shell=True)

def exec_path(path, cur_path):
    if path=="" or not os.path.exists(path) or not os.path.isfile(path):
        messagebox.showerror("エラー", 'ファイル"%s"がありません。' % path)
        return

    subprocess.Popen([os.path.abspath(path)], cwd=os.path.abspath(cur_path))

def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2-size[0]/2
    y = h/2-size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size+(x,y)))

def on_closing():
    global main_win
    if False:
        result = messagebox.askquestion("確認", "終了します。\nよろしいですか?")
    else:
        result = "yes"
    if result == "yes":
        write_config()
        main_win.destroy()

# config
def open_game_dlg():
    global game_path
    global game_path_entry
    path = filedialog.askdirectory()
    if path != "":
        if not os.path.exists(path) or not os.path.isdir(path):
            path = ""
        game_path_entry.delete(0, END)
        game_path_entry.insert(0, path)
        game_path = path

def open_game_explorer():
    if game_path=="" or not os.path.exists(game_path) or not os.path.isdir(game_path):
        messagebox.showerror("エラー", "ゲームパスを設定してください。")
        return

    open_dir(game_path)

def exec_game():
    if game_path=="" or not os.path.exists(game_path) or not os.path.isdir(game_path):
        messagebox.showerror("エラー", "ゲームパスを設定してください。")
        return

    exec_path("%s/Frostpunk.exe" % game_path, game_path)

# manage data
def backup_data():
    if game_path=="" or not os.path.exists(game_path) or not os.path.isdir(game_path):
        messagebox.showerror("エラー", "ゲームパスを設定してください。")
        return

    result = messagebox.askquestion("確認", "データをバックアップします。\nよろしいですか?", icon="warning")
    if result == "yes":
        path = "./backup"
        if os.path.exists(path):
            result = messagebox.askquestion("確認", "バックアップデータを上書きします。\nよろしいですか?", icon="warning")
            if result != "yes":
                messagebox.showinfo("情報", "データをバックアップしませんでした。", icon="warning")
                return
        else:
            os.mkdir(path)
        shutil.copy2("%s/common.idx" % game_path, "%s/common.idx" % path)
        shutil.copy2("%s/common.dat" % game_path, "%s/common.dat" % path)
        shutil.copy2("%s/localizations.idx" % game_path, "%s/localizations.idx" % path)
        shutil.copy2("%s/localizations.dat" % game_path, "%s/localizations.dat" % path)
        messagebox.showinfo("情報", 'フォルダ"%s"にバックアップしました。' % path)

def restore_data():
    if game_path=="" or not os.path.exists(game_path) or not os.path.isdir(game_path):
        messagebox.showerror("エラー", "ゲームパスを設定してください。")
        return

    path = "./backup"
    if not os.path.exists(path):
        messagebox.showerror("エラー", "バックアップデータがありません。")
        return

    result = messagebox.askquestion("確認", "データをリストアします。\nよろしいですか?", icon="warning")
    if result == "yes":
        shutil.copy2("%s/common.idx" % path, "%s/common.idx" % game_path)
        shutil.copy2("%s/common.dat" % path, "%s/common.dat" % game_path)
        shutil.copy2("%s/localizations.idx" % path, "%s/localizations.idx" % game_path)
        shutil.copy2("%s/localizations.dat" % path, "%s/localizations.dat" % game_path)
        messagebox.showinfo("情報", 'フォルダ"%s"からリストアしました。' % path)

def download_sheet():
    result = messagebox.askquestion("確認", "翻訳シートをWebサイトからダウンロードします。\nよろしいですか?")
    if result == "yes":
        path = "../lang/data/Frostpunk 翻訳作業所 - 翻訳.csv"
        if os.path.exists(path):
            result = messagebox.askquestion("確認", "翻訳シートを上書きします。\nよろしいですか?", icon="warning")
            if result != "yes":
                messagebox.showinfo("情報", "翻訳シートをダウンロードしませんでした。", icon="warning")
                return

        os.chdir("../lang/")
        try:
            subprocess.Popen(["python", "./fetch_sheet.py"]).wait()
        except OSError:
            subprocess.Popen(["./fetch_sheet.exe"]).wait()
        os.chdir("../general/")
        messagebox.showinfo("情報", "翻訳シートをダウンロードしました。")

def open_sheet():
    path = "../lang/data/Frostpunk 翻訳作業所 - 翻訳.csv"
    if not os.path.exists(path):
        messagebox.showerror("エラー", "翻訳シートがありません。\n一度ダウンロードする必要があります。")
        return

    open_csv(path)

def open_data_explorer():
    path = "./backup"
    if not os.path.exists(path):
        messagebox.showerror("エラー", "バックアップデータがありません。")
        return

    open_dir(path)

# patch
def patch_font():
    if game_path=="" or not os.path.exists(game_path) or not os.path.isdir(game_path):
        messagebox.showerror("エラー", "ゲームパスを設定してください。")
        return

    if not os.path.exists("./backup"):
        messagebox.showerror("エラー", "バックアップデータがありません。\n一度バックアップをする必要があります。")
        return

    result = messagebox.askquestion("確認", "フォントパッチを適応します。若干時間が掛かります。\nよろしいですか?", icon="warning")
    if result == "yes":
        os.chdir("../dat/")
        if False:
            path = game_path
        else:
            path = "../general/backup"

        # unpack
        shutil.copy2("%s/common.idx" % path, "./data/common.idx")
        shutil.copy2("%s/common.dat" % path, "./data/common.dat")
        if os.path.exists("./out/common"):
            shutil.rmtree("./out/common")
        try:
            subprocess.Popen(["python", "./unpack.py"]).wait()
        except OSError:
            subprocess.Popen(["./unpack.exe"]).wait()
        os.remove("./data/common.idx")
        os.remove("./data/common.dat")

        # binfont
        if not os.path.exists("../binfont/out/notosanscjksc-medium.otf.binfont"):
            subprocess.Popen(["../compile/unzip", "-d", "../binfont/out/", "../binfont/out/notosanscjksc-medium.otf.binfont.zip"]).wait()
        shutil.copy2("../binfont/out/notosanscjksc-medium.otf.binfont", "./out/common/notosanscjksc-medium.otf.binfont")

        # pack
        try:
            subprocess.Popen(["python", "./pack.py"]).wait()
        except OSError:
            subprocess.Popen(["./pack.exe"]).wait()
        shutil.rmtree("./out/common")

        # copy
        shutil.copy2("./out/common.idx", "%s/common.idx" % game_path)
        shutil.copy2("./out/common.dat", "%s/common.dat" % game_path)
        os.remove("./out/common.idx")
        os.remove("./out/common.dat")

        os.chdir("../general/")
        messagebox.showinfo("情報", "フォントパッチを適応しました。")

def patch_lang():
    if game_path=="" or not os.path.exists(game_path) or not os.path.isdir(game_path):
        messagebox.showerror("エラー", "ゲームパスを設定してください。")
        return

    if not os.path.exists("./backup"):
        messagebox.showerror("エラー", "バックアップデータがありません。\n一度バックアップをする必要があります。")
        return

    if not os.path.exists("../lang/data/Frostpunk 翻訳作業所 - 翻訳.csv"):
        messagebox.showerror("エラー", "翻訳シートがありません。\n一度ダウンロードする必要があります。")
        return

    result = messagebox.askquestion("確認", "翻訳パッチを適応します。\nよろしいですか?", icon="warning")
    if result == "yes":
        result = messagebox.askquestion("確認", "Googleによる機械翻訳のデータを含めますか?")
        wmt = result == "yes"
        os.chdir("../dat/")
        if False:
            path = game_path
        else:
            path = "../general/backup"

        # unpack
        shutil.copy2("%s/localizations.idx" % path, "./data/localizations.idx")
        shutil.copy2("%s/localizations.dat" % path, "./data/localizations.dat")
        if os.path.exists("./out/localizations"):
            shutil.rmtree("./out/localizations")
        try:
            subprocess.Popen(["python", "./unpack.py"]).wait()
        except OSError:
            subprocess.Popen(["./unpack.exe"]).wait()
        os.remove("./data/localizations.idx")
        os.remove("./data/localizations.dat")

        # lang
        os.chdir("../lang/")
        shutil.copy2("../dat/out/localizations/english.lang", "./data/english.lang")
        shutil.copy2("../dat/out/localizations/french.lang", "./data/french.lang")
        shutil.copy2("../dat/out/localizations/german.lang", "./data/german.lang")
        shutil.copy2("../dat/out/localizations/spanish.lang", "./data/spanish.lang")
        shutil.copy2("../dat/out/localizations/polish.lang", "./data/polish.lang")
        shutil.copy2("../dat/out/localizations/russian.lang", "./data/russian.lang")
        shutil.copy2("../dat/out/localizations/chinese.lang", "./data/chinese.lang")
        try:
            subprocess.Popen(["python", "./lang2csv.py"]).wait()
        except OSError:
            subprocess.Popen(["./lang2csv.exe"]).wait()
        os.remove("./data/english.lang")
        os.remove("./data/french.lang")
        os.remove("./data/german.lang")
        os.remove("./data/spanish.lang")
        os.remove("./data/polish.lang")
        os.remove("./data/russian.lang")
        os.remove("./data/chinese.lang")
        try:
            subprocess.Popen(["python", "./make_ja.py"]).wait()
        except OSError:
            subprocess.Popen(["./make_ja.exe"]).wait()
        shutil.copy2("./out/english.lang", "../dat/out/localizations/english.lang")
        shutil.copy2("./out/french.lang", "../dat/out/localizations/french.lang")
        shutil.copy2("./out/german.lang", "../dat/out/localizations/german.lang")
        shutil.copy2("./out/spanish.lang", "../dat/out/localizations/spanish.lang")
        shutil.copy2("./out/polish.lang", "../dat/out/localizations/polish.lang")
        shutil.copy2("./out/russian.lang", "../dat/out/localizations/russian.lang")
        if wmt:
            shutil.copy2("./out/japanese_wmt.lang", "../dat/out/localizations/chinese.lang")
        else:
            shutil.copy2("./out/japanese.lang", "../dat/out/localizations/chinese.lang")
        os.remove("./out/english.lang")
        os.remove("./out/french.lang")
        os.remove("./out/german.lang")
        os.remove("./out/spanish.lang")
        os.remove("./out/polish.lang")
        os.remove("./out/russian.lang")
        os.remove("./out/chinese.lang")
        os.remove("./out/japanese.lang")
        os.remove("./out/japanese_wmt.lang")
        os.chdir("../dat/")

        # pack
        try:
            subprocess.Popen(["python", "./pack.py"]).wait()
        except OSError:
            subprocess.Popen(["./pack.exe"]).wait()
        shutil.rmtree("./out/localizations")

        # copy
        shutil.copy2("./out/localizations.idx", "%s/localizations.idx" % game_path)
        shutil.copy2("./out/localizations.dat", "%s/localizations.dat" % game_path)
        os.remove("./out/localizations.idx")
        os.remove("./out/localizations.dat")

        os.chdir("../general/")
        messagebox.showinfo("情報", "翻訳パッチを適応しました。")

def open_lang():
    path = "../lang/out/lang.csv"
    if not os.path.exists(path):
        messagebox.showerror("エラー", "ゲームの翻訳シートがありません。\n一度翻訳パッチを適応する必要があります。")
        return

    open_csv(path)

# link
def open_game_web():
    if False:
        result = messagebox.askquestion("確認", "FrostpunkのWebサイトを開きます。\nよろしいですか?")
        if result != "yes":
            return

    webbrowser.open_new(game_url)

def open_tool_web():
    if False:
        result = messagebox.askquestion("確認", "MODツールのWebサイトを開きます。\nよろしいですか?")
        if result != "yes":
            return

    webbrowser.open_new(tool_url)

def open_sheet_web():
    if False:
        result = messagebox.askquestion("確認", "翻訳シートのWebサイトを開きます。\nよろしいですか?")
        if result != "yes":
            return

    webbrowser.open_new(sheet_url)

def main():
    global main_win
    global game_path
    global game_path_entry
    version_fg_color = "darkblue"
    inf_fg_color = "darkgreen"
    risk_fg_color = "darkred"
    hover_fg_color = "blue"
    hover_risk_fg_color = "red"

    # main window
    main_win = Tk()
    main_win.title("Frostpunk用総合MODツール")
    main_win.geometry("380x510")
    main_win.resizable(0,0)
    main_win.protocol("WM_DELETE_WINDOW", on_closing)
    center(main_win)

    # main frame
    main_frame = Frame(main_win, highlightthickness=1,highlightbackground="gray")
    main_frame.pack(padx=4,pady=4,ipadx=20,ipady=20, fill=BOTH)

    # version
    version_label = Label(main_frame, text="ver %s" % version, fg=version_fg_color)
    version_label.pack(padx=12, anchor=E)

    # config
    config_frame = LabelFrame(main_frame, text="設定")
    config_frame.pack(padx=12,pady=4,ipadx=12,ipady=4, fill=X)
    game_path_frame = Frame(config_frame)
    game_path_frame.pack()
    game_path_label = Label(game_path_frame, text="ゲームパス:")
    game_path_label.pack(side=LEFT)
    game_path_entry = Entry(game_path_frame, relief=FLAT, width=40)
    game_path_entry.pack(side=LEFT)
    open_game_dlg_button = Button(game_path_frame, text="...", command=open_game_dlg, relief=FLAT, cursor="hand2")
    org_fg_color = open_game_dlg_button.cget("foreground")
    open_game_dlg_button.bind("<Enter>", lambda event, h=open_game_dlg_button: h.configure(fg=hover_fg_color))
    open_game_dlg_button.bind("<Leave>", lambda event, h=open_game_dlg_button: h.configure(fg=org_fg_color))
    open_game_dlg_button.pack()
    open_game_explorer_button = Button(config_frame, text="ゲームフォルダを開く", command=open_game_explorer, relief=FLAT, cursor="hand2")
    open_game_explorer_button.bind("<Enter>", lambda event, h=open_game_explorer_button: h.configure(fg=hover_fg_color))
    open_game_explorer_button.bind("<Leave>", lambda event, h=open_game_explorer_button: h.configure(fg=org_fg_color))
    open_game_explorer_button.pack()
    if False:
        exec_game_button = Button(config_frame, text="ゲームを起動", command=exec_game, relief=FLAT, cursor="hand2")
        exec_game_button.bind("<Enter>", lambda event, h=exec_game_button: h.configure(fg=hover_fg_color))
        exec_game_button.bind("<Leave>", lambda event, h=exec_game_button: h.configure(fg=org_fg_color))
        exec_game_button.pack()

    # manage data
    manage_data_frame = LabelFrame(main_frame, text="データ管理")
    manage_data_frame.pack(padx=12,pady=4,ipadx=12,ipady=4, fill=X)
    backup_button = Button(manage_data_frame, text="パッチに関係するデータ(4ファイル)をバックアップ", command=backup_data, relief=FLAT, cursor="hand2")
    backup_button.bind("<Enter>", lambda event, h=backup_button: h.configure(fg=hover_fg_color))
    backup_button.bind("<Leave>", lambda event, h=backup_button: h.configure(fg=org_fg_color))
    backup_button.pack()
    restore_button = Button(manage_data_frame, text="パッチに関係するデータ(4ファイル)をリストア", command=restore_data, relief=FLAT, cursor="hand2", fg=risk_fg_color)
    restore_button.bind("<Enter>", lambda event, h=restore_button: h.configure(fg=hover_risk_fg_color))
    restore_button.bind("<Leave>", lambda event, h=restore_button: h.configure(fg=risk_fg_color))
    restore_button.pack()
    open_data_explorer_button = Button(manage_data_frame, text="バックアップデータフォルダを開く", command=open_data_explorer, relief=FLAT, cursor="hand2")
    open_data_explorer_button.bind("<Enter>", lambda event, h=open_data_explorer_button: h.configure(fg=hover_fg_color))
    open_data_explorer_button.bind("<Leave>", lambda event, h=open_data_explorer_button: h.configure(fg=org_fg_color))
    open_data_explorer_button.pack()
    download_sheet_button = Button(manage_data_frame, text="翻訳シート(.csv)をWebサイトからダウンロード", command=download_sheet, relief=FLAT, cursor="hand2")
    download_sheet_button.bind("<Enter>", lambda event, h=download_sheet_button: h.configure(fg=hover_fg_color))
    download_sheet_button.bind("<Leave>", lambda event, h=download_sheet_button: h.configure(fg=org_fg_color))
    download_sheet_button.pack()
    open_sheet_button = Button(manage_data_frame, text="ダウンロードした翻訳シート(.csv)を開く", command=open_sheet, relief=FLAT, cursor="hand2")
    open_sheet_button.bind("<Enter>", lambda event, h=open_sheet_button: h.configure(fg=hover_fg_color))
    open_sheet_button.bind("<Leave>", lambda event, h=open_sheet_button: h.configure(fg=org_fg_color))
    open_sheet_button.pack()

    # patch
    patch_frame = LabelFrame(main_frame, text="パッチ")
    patch_frame.pack(padx=12,pady=4,ipadx=12,ipady=4, fill=X)
    patch_font_button = Button(patch_frame, text="フォント(binfont)パッチを適応", command=patch_font, relief=FLAT, cursor="hand2", fg=risk_fg_color)
    patch_font_button.bind("<Enter>", lambda event, h=patch_font_button: h.configure(fg=hover_risk_fg_color))
    patch_font_button.bind("<Leave>", lambda event, h=patch_font_button: h.configure(fg=risk_fg_color))
    patch_font_button.pack()
    patch_lang_button = Button(patch_frame, text="翻訳(lang)パッチを適応", command=patch_lang, relief=FLAT, cursor="hand2", fg=risk_fg_color)
    patch_lang_button.bind("<Enter>", lambda event, h=patch_lang_button: h.configure(fg=hover_risk_fg_color))
    patch_lang_button.bind("<Leave>", lambda event, h=patch_lang_button: h.configure(fg=risk_fg_color))
    patch_lang_button.pack()
    open_lang_button = Button(patch_frame, text="ゲームの翻訳シート(.csv)を開く", command=open_lang, relief=FLAT, cursor="hand2")
    open_lang_button.bind("<Enter>", lambda event, h=open_lang_button: h.configure(fg=hover_fg_color))
    open_lang_button.bind("<Leave>", lambda event, h=open_lang_button: h.configure(fg=org_fg_color))
    open_lang_button.pack()

    # link
    link_frame = LabelFrame(main_frame, text="Webサイト")
    link_frame.pack(padx=12,pady=4,ipadx=12,ipady=4, fill=X)
    if False:
        open_game_web_button = Button(link_frame, text="FrostpunkのWebサイトを開く", command=open_game_web, relief=FLAT, cursor="hand2")
        open_game_web_button.bind("<Enter>", lambda event, h=open_game_web_button: h.configure(fg=hover_fg_color))
        open_game_web_button.bind("<Leave>", lambda event, h=open_game_web_button: h.configure(fg=org_fg_color))
        open_game_web_button.pack()
    open_tool_web_button = Button(link_frame, text="MODツールのWebサイトを開く", command=open_tool_web, relief=FLAT, cursor="hand2")
    open_tool_web_button.bind("<Enter>", lambda event, h=open_tool_web_button: h.configure(fg=hover_fg_color))
    open_tool_web_button.bind("<Leave>", lambda event, h=open_tool_web_button: h.configure(fg=org_fg_color))
    open_tool_web_button.pack()
    open_sheet_web_button = Button(link_frame, text="翻訳シートのWebサイトを開く", command=open_sheet_web, relief=FLAT, cursor="hand2")
    open_sheet_web_button.bind("<Enter>", lambda event, h=open_sheet_web_button: h.configure(fg=hover_fg_color))
    open_sheet_web_button.bind("<Leave>", lambda event, h=open_sheet_web_button: h.configure(fg=org_fg_color))
    open_sheet_web_button.pack()

    # information
    inf_label = Label(main_frame, text="翻訳シート管理人様、翻訳有志諸氏に多大なる感謝を！", fg=inf_fg_color)
    inf_label.pack()

    # init
    read_config()
    if game_path != "":
        game_path_entry.insert(0, game_path)
    elif os.path.exists(def_app_path1):
        game_path_entry.insert(0, def_app_path1)
        game_path = def_app_path1
    elif os.path.exists(def_app_path2):
        game_path_entry.insert(0, def_app_path2)
        game_path = def_app_path2

    main_win.mainloop()

main()
