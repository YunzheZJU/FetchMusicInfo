# -*- coding: utf-8 -*-
import os
import re
import requests
import urllib
import shutil


def fetchCover(text):
    reg = r'<div class="summary-pic">.*?(https.*.jpg).*?picAlbumBtn'
    result = re.search(reg, text)
    if result:
        img_addr = result.group(1)
        r = requests.get(img_addr, stream=True)
        try:
            with open(os.path.join(dir_cover, str(counter) + "." + songname + "." + img_addr.split(".")[-1]), "wb") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)
                    f.flush()
        finally:
            if f:
                f.close()
        return 1
    print "Error in fetching cover."
    return 0


def fetchText(keyword):
    # print keyword
    # print type(keyword)
    keyword = keyword.encode("utf-8")
    # print keyword
    # print type(keyword)
    session = requests.session()
    headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'baike.baidu.com',
            'Pragma': 'no-cache',
            'Referer': 'https://baike.baidu.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    print "Waiting for session..."
    resp = session.get('https://baike.baidu.com/search/word?word=' + urllib.quote(keyword), headers=headers)
    print "Get session."
    text = resp.content.replace("\n", "")
    reg = r'searchResult'
    # print type(text)
    # print urllib.quote(keyword)
    if re.search(reg, text):
        print "Error in searching keyword."
        return None
    if fetchCover(text) == 0:
        return None
    # reg = r'summary-pic'
    # if re.search(reg, text) is None:
    #     print "Error in finding cover."
    #     return None
    try:
        reg = r'<div class="lemma-summary" label-module="lemmaSummary">(.*?)<div class="configModuleBanner">'
        text = re.search(reg, text).group(1)
        reg = r'<.*?>'
        search_result = re.search(reg, text)
        # print "Replacing tags..."
        while search_result:
            text = text.replace(search_result.group(0), "")
            search_result = re.search(reg, text)
        reg = r'\[\d+\]'
        search_result = re.search(reg, text)
        # print "Replacing numbers..."
        while search_result:
            text = text.replace(search_result.group(0), "")
            search_result = re.search(reg, text)
        # print "Replacing spaces..."
        # print text
        reg = r'&nbsp;'
        search_result = re.search(reg, text)
        # print search_result
        if search_result is not None:
            # print "None"
            text = text.replace(search_result.group(0), "")
        return text
    except:
        print "Error in replacing."
        return None


dir_original = os.path.join(os.path.abspath("."), "original")
dir_text = os.path.join(os.path.abspath("."), "text")
dir_music = os.path.join(os.path.abspath("."), "music")
dir_cover = os.path.join(os.path.abspath("."), "cover")
if not os.path.exists(dir_original):
    print "No materials!"
    exit(0)
for path in [dir_text, dir_music, dir_cover]:
    if not os.path.exists(path):
        os.mkdir(path)
fileList = os.listdir(dir_original)
if "Thumbs.db" in fileList:
    fileList.remove("Thumbs.db")
counter = 1
for filename in fileList:
    # reg = r'\d+\.(.*?)\s*-\s*(.*?)(\s|\.|\(|\xa3\xa8)'
    reg = r'\d+\.(.*)\.+'
    songname = re.match(reg, filename).group(1)
    keyword = songname.decode("gbk")
    print keyword
    # print type(keyword)
    Text = fetchText(keyword)
    if Text is None:
        print songname.decode("gbk") + "  ERROR"
        continue
    with open(os.path.join(dir_text, str(counter) + "." + songname + ".txt"), "w") as f:
        f.write(Text)
    shutil.move(os.path.join(dir_original, filename), os.path.join(dir_music, str(counter) + "." + songname + ".mp3"))
    print songname.decode("gbk") + "  OK"
    counter += 1

