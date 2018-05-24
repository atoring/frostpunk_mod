#!/usr/bin/python
# coding: utf-8

# mod
from common import *
import gui

def main():
    "main"
    log("start")
    log("prog path", get_prog_path())
    gui.main()
    log("end")

if __name__ == "__main__":
    main()
