# -*- coding: utf-8 -*-
import os
import re
from PIL import Image


def process(path):
    fileList = os.listdir(path)
    if "Thumbs.db" in fileList:
        fileList.remove("Thumbs.db")
    regSong = r'(\d+)\..*?\.mp3'
    regPic = r'(\d+)\..*?\.(jpg|png)'
    regTxt = r'(\d+)\.(.*?)\.txt'
    for filename in fileList:
        songFile = re.match(regSong, filename)
        picFile = re.match(regPic, filename)
        txtFile = re.match(regTxt, filename)
        oldpath = os.path.join(path, filename)
        print filename
        if songFile:
            songnumber = songFile.group(1)
            newpath = os.path.join(path, "0" * (3 - len(songnumber)) + songnumber + ".mp3")
            # Rename
            os.rename(oldpath, newpath)
        elif picFile:
            picnumber = picFile.group(1)
            pictype = picFile.group(2)
            newpath = os.path.join(path, "0" * (3 - len(picnumber)) + picnumber + ".jpg")
            if pictype == "png":
                # Convert and remove the original one
                Image.open(oldpath).save(newpath)
                os.remove(oldpath)
            else:
                # Should be .jpg file
                # Rename
                os.rename(oldpath, newpath)
        elif txtFile:
            txtnumber = txtFile.group(1)
            txtname = txtFile.group(2)
            with open(oldpath, 'r') as f:
                lines = f.readlines()
                newlines = []
                for line in lines:
                    newlines.append(line.decode("utf-8").encode('gb18030'))
                # print singleLine.decode("gbk")
                # print newlines
            with open(oldpath, 'w') as f:
                f.write(txtname + "\n")
                f.write(newlines[0])
            newpath = os.path.join(path, "0" * (3 - len(txtnumber)) + txtnumber + ".txt")
            # Rename
            os.rename(oldpath, newpath)


# Prepare
dir_like = os.path.join(os.path.abspath("."), "Like")
dir_dislike = os.path.join(os.path.abspath("."), "Dislike")
if not os.path.exists(dir_like):
    print "No like folder!"
    exit(0)
if not os.path.exists(dir_dislike):
    print "No like folder!"
    exit(0)

# Start
for dir in [dir_like, dir_dislike]:
    process(dir)
