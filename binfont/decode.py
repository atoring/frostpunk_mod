#!/usr/bin/python
# coding: utf-8

# ./data/notosanscjksc-medium.otf.binfontをデコードして./out/にファイルを生成します。

import codecs
import struct
from PIL import Image

def read_bin(path):
    print("read file: %s" % path)
    try:
        f = open(path, "rb")
    except IOError:
        print("error: file open error: %s" % path)
        quit()
    data = f.read()
    f.close()
    print("read size: %xh" % len(data))
    return data

def write_bin(path, data):
    print("write file: %s" % path)
    try:
        f = open(path, "wb")
    except IOError:
        print("error: file open error: %s" % path)
        quit()
    f.write(data)
    f.close()
    print("write size: %xh" % len(data))

def write_png(path, data, width, height, bpp):
    print("write file: %s" % path)
#    img = Image.frombytes("RGBA", (width,height), data, "raw", "RGBA", 0, 1)
    img = Image.frombytes("RGB", (width,height), data, "raw", "RGBX", 0, 1)
    img.save(path, "png")

def write_txt(path, encode, data):
    print("write file: %s" % path)
    try:
        f = codecs.open(path, "w", encode)
    except IOError:
        print("error: file open error: %s" % path)
        quit()
    for d in data:
        f.write(d)
    f.close()
    print("write len: %d" % len(data))

def write_chars(path, data):
    chrs = struct.unpack("<I", data[:4])[0]
    print("chrs: %d" % chrs)
    inf = []
    tmp = struct.unpack("<fff", data[4+chrs*32:16+chrs*32])
    inf.append("%f %f %f\n" % (tmp[0],tmp[1],tmp[2]))
    for i in range(chrs):
        left,right,top,bottom,width,offset_left,offset_top,code,tex = struct.unpack("<fffffffHH", data[4+i*32:36+i*32])
        inf.append("code=%04x[%c] tex=%d left=%f right=%f top=%f bottom=%f width=%f offset_left=%f offset_top=%f\n" % (code,code,tex,left,right,top,bottom,width,offset_left,offset_top))
    write_txt(path, "utf_8_sig", inf) # with bom

def write_codes(path, data):
    chrs = struct.unpack("<I", data[:4])[0]
    print("chrs: %d" % chrs)
    codes = []
    for i in range(chrs):
        codes.append(data[32+i*32:34+i*32].decode("utf_16_le"))
    write_txt("%s_utf16.txt" % path, "utf_16_le", codes)
    write_txt("%s_utf8.txt" % path, "utf_8_sig", codes) # with bom

def decode():
    width = 4096
    bpp = 32
    data = read_bin("./data/notosanscjksc-medium.otf.binfont")

    magic,ver,texs = struct.unpack("<III", data[:12])
    print("magic: %xh" % magic)
    print("ver: %d" % ver)
    print("texs: %d" % texs)
    offset = 12+texs*4
#    write_bin("./out/head.bin", data[:offset])
    for i in range(texs):
        height = struct.unpack("<I", data[12+i*4:16+i*4])[0]
        print("height: %d" % height)
        size = width*height*(bpp//8)
        tex = data[offset:offset+size]
#        write_bin("./out/tex%d.bin" % i, tex)
        write_png("./out/tex%d.png" % i, tex, width, height, bpp)
        offset += size

#    write_bin("./out/chars.bin", data[offset:])
    write_chars("./out/chars.txt", data[offset:])
    write_codes("./out/codes", data[offset:])

decode()
