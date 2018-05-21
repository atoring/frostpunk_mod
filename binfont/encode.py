#!/usr/bin/python
# coding: utf-8

# ./data/font*.*をエンコードして./out/notosanscjksc-medium.otf.binfontを生成します。
# フォントサイズやオフセットなど使用フォントにより調整する必要があります。

# for https://github.com/libgdx/libgdx/wiki/Hiero
# https://github.com/libgdx/libgdx/wiki/Distance-field-fonts

import codecs
import re
import struct
from PIL import Image

def read_txt(path):
    print("read file: %s" % path)
    try:
        f = codecs.open(path, "r", "cp932")
    except IOError:
        print("error: file open error: %s" % path)
        quit()
    data = f.readlines()
    f.close()
    print("read lines: %d" % len(data))
    return data

def read_fnt_txt(path):
    data = read_txt(path)

    _pageNames = {}
    _chars = {}
    for str in data:
        str = str.rstrip("\r\n")
#        print(str)

        m = re.search('^page[ ]+id=([0-9]+)[ ]+file="(.+)"$', str)
        if m:
            id = int(m.group(1))
            file = m.group(2)
            _pageNames[id] = file
            print("pageNames: %d=\"%s\"" % (id,file))

        m = re.search("^chars[ ]+count=([0-9]+)$", str)
        if m:
            numChars = int(m.group(1))
            print("numChars: %d" % numChars)

        m = re.search(r"^char[ ]+id=([0-9]+)[ ]+x=([0-9]+)[ ]+y=([0-9]+)[ ]+width=([0-9]+)[ ]+height=([0-9]+)[ ]+xoffset=([0-9\-]+)[ ]+yoffset=([0-9\-]+)[ ]+xadvance=([0-9]+)[ ]+page=([0-9]+)[ ]+chnl=([0-9]+)[ ]+$", str)
        if m:
            id,x,y,width,height,xoffset,yoffset,xadvance,page,chnl = tuple(int(s) for s in m.groups())
            _chars[id] = {"id":id,"x":x,"y":y,"width":width,"height":height,"xoffset":xoffset,"yoffset":yoffset,"xadvance":xadvance,"page":page,"chnl":chnl}

    pageNames = [_pageNames[k] for k in sorted(_pageNames.keys())]
    chars = [_chars[k] for k in sorted(_chars.keys())]
    return pageNames, chars

def read_pngs(base, path, width, height):
    print("width: %d" % width)
    print("height: %d" % height)

    img = Image.new("RGBA", (width,height))
    pos = [(0,0),(width//2,0),(0,height//2),(width//2,height//2)]
    cnt = 0
    for p in path:
        _path = "%s%s" % (base,p)
        print("read file: %s" % _path)
        _img = Image.open(_path)
        if _img.size != (width//2,height//2):
            print("error: image size")
            print(_img.size)
            quit()
        img.paste(_img, pos[cnt])
        cnt += 1

    if True:    # fix
        r,g,b,a = img.split()
        z = a.point(lambda p:0)
        img = Image.merge("RGBA", (a,a,a,z))

    data = img.tobytes()
    print("size: %xh" % len(data))
    return width, height, data

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

def encode():
    width = 4096
    height = 4096
    bpp = 32
    tex_file,chrs = read_fnt_txt("./data/font.fnt")

    bin = bytearray()
    magic,ver,texs = (0x35150f8a,9,len(tex_file))
    _texs = (texs+3)//4
    bin.extend(struct.pack("<III", magic,ver,_texs))

    tex = bytearray()
    for i in range(_texs):
        print("tex group: %d" % i)
        w,h,d = read_pngs("./data/", tex_file[i*4:(i+1)*4], width, height)
        if w!=width or h!=height:
            print("error: size")
            quit()
        bin.extend(struct.pack("<I", h))
        tex.extend(d)
    bin.extend(tex)

    bin.extend(struct.pack("<I", len(chrs)))
    for c in chrs:
        id,x,y,w,h,xoffset,yoffset,xadvance,page,chnl = (c["id"],c["x"],c["y"],c["width"],c["height"],c["xoffset"],c["yoffset"],c["xadvance"],c["page"],c["chnl"])

        if True:    # fix
            p = 8
            xadvance -= p*2

        if page%4 == 1:
            x += width//2
        if page%4 == 2:
            y += height//2
        if page%4 == 3:
            x += width//2
            y += height//2
        page //= 4

        left = x
        right = x+w
        top = y
        bottom = y+h
        _width = xadvance
        offset_left = xoffset
        offset_top = yoffset
        code = id
        tex = page

        if False:    # fix
            p = 3
            if w > p:
                offset_left += p
                left += p
                if w > p*2:
                    right -= p
            p = 6
            if h > p:
                offset_top += p
                top += p
                if h > p*2:
                    bottom -= p

        if False:    # fix
            p = 12
            left -= p
            right += p
            top -= p
            bottom += p
            offset_left += p
            offset_top += p

        # ja patch
        if code == 0xff0c: # 「，」
            bin.extend(struct.pack("<fffffffHH", 0,0,0,0, 0,0,0, code,0xffff))
        else:
            bin.extend(struct.pack("<fffffffHH", left,right,top,bottom,_width,offset_left,offset_top,code,tex))
    bin.extend(struct.pack("<fff", 46.25,0.0,7.03125))

    write_bin("./out/notosanscjksc-medium.otf.binfont", bin)

encode()
