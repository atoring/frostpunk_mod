#!/usr/bin/python
# coding: utf-8

# ./data/font*.pngを加工して、./out/font*.pngを生成します。(encode.py用データ)

import glob
import os
from PIL import Image
from PIL import ImageFilter

def read_png(path):
    print("read file: %s" % path)
    img = Image.open(path).convert("RGBA")
    print("size: %dx%d" % img.size)
    return img

def fix_img(img):
    tmp = img.filter(ImageFilter.MaxFilter(3))
    tmp = tmp.filter(ImageFilter.GaussianBlur(1.45))
    tmp = tmp.point(lambda p:p*0.7)
    r,g,b,a = img.split()
    x = r.point(lambda p:0xff)
    img = Image.merge("RGBA", (x,x,x,r))
    img = Image.alpha_composite(tmp, img)
    r,g,b,a = img.split()
    p = r.point(lambda p:p*0.6)
    z = r.point(lambda p:0)
    img = Image.merge("RGBA", (x,p,z,x))
    return img

def write_png(path, img):
    print("write file: %s" % path)
    img.save(path, "png")

def fix_png():
    path = "./data/font_*.png"
    files = glob.glob(path)
    files.sort()
    for f in files:
        img = read_png(f)
        img = fix_img(img)
        write_png("./out/%s" % os.path.split(f)[1], img)

fix_png()
