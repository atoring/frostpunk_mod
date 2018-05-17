#!/usr/bin/python
# coding: utf-8

# ./data/font*.*をエンコードして./out/notosanscjksc-medium.otf.binfontを生成します。
# フォントサイズやオフセットなど使用フォントにより調整する必要があります。

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

def read_fnt(path):
    bin = read_bin(path)

    # see: http://www.angelcode.com/products/bmfont/doc/file_format.html
    # head
    magic = struct.unpack("<BBB", bin[:3])
    print("magic: %02xh,%02xh,%02xh" % (magic[0],magic[1],magic[2]))
    if magic != (0x42,0x4d,0x46):   # "BMF"
        print("error: magic")
        quit()
    ver = struct.unpack("B", bin[3:4])[0]
    print("ver: %d" % ver)
    if ver != 3:
        print("error: ver")
        quit()

    # block
    offset = 4
    while offset < len(bin):
        blockId,blockSize = struct.unpack("<BI", bin[offset:offset+5])
        offset += 5
        block_offset = offset
        print("blockId: %xh" % blockId)
        print("blockSize: %d" % blockSize)

        # Block type 1: info
        if blockId == 1:
            fontSize,bitField,charSet,stretchH,aa,paddingUp,paddingRight,paddingDown,paddingLeft,spacingHoriz,spacingVert,outline = struct.unpack("<HBBHBBBBBBBB", bin[offset:offset+14])
            offset += 14
            print("fontSize: %d" % fontSize)
            print("bitField: %xh" % bitField)
            print("charSet: %d" % charSet)
            print("stretchH: %d" % stretchH)
            print("aa: %d" % aa)
            print("paddingUp: %d" % paddingUp)
            print("paddingRight: %d" % paddingRight)
            print("paddingDown: %d" % paddingDown)
            print("paddingLeft: %d" % paddingLeft)
            print("spacingHoriz: %d" % spacingHoriz)
            print("spacingVert: %d" % spacingVert)
            print("outline: %d" % outline)
            fontName = bin[offset:].split(b"\0")[0].decode("ascii")
            print("fontName: \"%s\"" % fontName)

        # Block type 2: common
        if blockId == 2:
            lineHeight,base,scaleW,scaleH,pages,bitField,alphaChnl,redChnl,greenChnl,blueChnl = struct.unpack("<HHHHHBBBBB", bin[offset:offset+15])
            print("lineHeight: %d" % lineHeight)
            print("base: %d" % base)
            print("scaleW: %d" % scaleW)
            print("scaleH: %d" % scaleH)
            print("pages: %d" % pages)
            print("bitField: %xh" % bitField)
            print("alphaChnl: %d" % alphaChnl)
            print("redChnl: %d" % redChnl)
            print("greenChnl: %d" % greenChnl)
            print("blueChnl: %d" % blueChnl)

        # Block type 3: pages
        if blockId == 3:
            p = bin[offset:].split(b"\0")
            pageNames = []
            for i in range(pages):
                _p = p[i].decode("ascii")
                pageNames.append(_p)
                print("pageNames: \"%s\"" % _p)

        # Block type 4: chars
        if blockId == 4:
            numChars = blockSize//20
            print("numChars: %d" % numChars)
            chars = []
            for i in range(numChars):
                id,x,y,width,height,xoffset,yoffset,xadvance,page,chnl = struct.unpack("<IHHHHhhhBB", bin[offset:offset+20])
                chars.append({"id":id,"x":x,"y":y,"width":width,"height":height,"xoffset":xoffset,"yoffset":yoffset,"xadvance":xadvance,"page":page,"chnl":chnl})
                offset += 20

        # Block type 5: kerning pairs
        if blockId == 5:
            numKers = blockSize//10
            print("numKers: %d" % numKers)
            kers = []
            for i in range(numKers):
                first,second,amount = struct.unpack("<IIh", bin[offset:offset+10])
                kers.append({"first":first,"second":second,"amount":amount})
                offset += 10

        offset = block_offset + blockSize

    return pageNames, chars

def read_png(path):
    print("read file: %s" % path)
    img = Image.open(path).convert("RGBA")
    width = img.width
    print("width: %d" % width)
    height = img.height
    print("height: %d" % height)
    if True:    # fix
        r,g,b,a = img.split()
        z = a.point(lambda p:0)
        img = Image.merge("RGBA", (r,g,b,z))
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
    bpp = 32
    tex_file,chrs = read_fnt("./data/font.fnt")

    bin = bytearray()
    magic,ver,texs = (0x35150f8a,9,len(tex_file))
    bin.extend(struct.pack("<III", magic,ver,texs))
    tex = bytearray()
    for t in tex_file:
#        w,h,d = read_png("./data/%s" % t)
        w,h,d = read_png("./out/%s" % t)
        if w != width:
            print("error: width")
            quit()
        bin.extend(struct.pack("<I", h))
        tex.extend(d)
    bin.extend(tex)
    bin.extend(struct.pack("<I", len(chrs)))
    tmp = bytearray()
    for c in chrs:
        id,x,y,w,h,xoffset,yoffset,xadvance,page,chnl = (c["id"],c["x"],c["y"],c["width"],c["height"],c["xoffset"],c["yoffset"],c["xadvance"],c["page"],c["chnl"])
        left = x
        right = x+w
        top = y
        bottom = y+h
        _width = xadvance
        offset_left = xoffset
        offset_top = yoffset
        code = id
        tex = page
        if True:    # fix
            if w > 3:
                offset_left += 3
                left += 3
                if w > 3*2:
                    right -= 3
            if h > 6:
                offset_top += 6
                top += 6
                if h > 6*2:
                    bottom -= 6
        # ja patch
        if code == 0x3001: # 「、」
            tmp = struct.pack("<fffffffHH", left,right,top,bottom,_width,offset_left,offset_top,0xff0c,tex)
        if code == 0xff0c: # 「，」
            bin.extend(tmp)
        else:
            bin.extend(struct.pack("<fffffffHH", left,right,top,bottom,_width,offset_left,offset_top,code,tex))
    bin.extend(struct.pack("<fff", 46.25,0.0,7.03125))

    write_bin("./out/notosanscjksc-medium.otf.binfont", bin)

encode()
