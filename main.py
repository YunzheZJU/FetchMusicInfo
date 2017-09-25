# -*- coding: utf-8 -*-
import os
import re
import requests
import urllib
import shutil


def fetchCover(text):
    # reg = r'<div class="summary-pic">.*?(https.*.jpg).*?picAlbumBtn'
    reg = r'class="image">.*?src="(https.*?)"'
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
    print urllib.quote(keyword).replace("%20", "+")
    session = requests.session()
    # headers = {
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #         'Accept-Encoding': 'gzip, deflate, br',
    #         'Accept-Language': 'zh-CN,zh;q=0.8',
    #         'Cache-Control': 'no-cache',
    #         'Connection': 'keep-alive',
    #         'DNT': '1',
    #         'Host': 'baike.baidu.com',
    #         'Pragma': 'no-cache',
    #         'Referer': 'https://baike.baidu.com/',
    #         'Upgrade-Insecure-Requests': '1',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    # }
    headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'zh.moegirl.org',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    print "Waiting for session..."
    # resp = session.get('https://baike.baidu.com/search/word?word=' + urllib.quote(keyword), headers=headers)
    resp = session.get('https://zh.moegirl.org/index.php?search=' + urllib.quote(keyword), headers=headers)
    print "Get session."
    text = resp.content.replace("\n", "")
    # reg = r'searchResult'
    reg = r'search-results'
    # print type(text)
    if re.search(reg, text):
        reg = r'<div class=\'mw-search-result-heading\'><a href="(.*?)"'
        result = re.search(reg, text)
        if result:
            text = session.get('https://zh.moegirl.org' + result.group(1)).content.replace("\n", "")
        else:
            print "Error in searching keyword."
            return None
    if fetchCover(text) == 0:
        return None
    # reg = r'summary-pic'
    # if re.search(reg, text) is None:
    #     print "Error in finding cover."
    #     return None
    try:
        # reg = r'<div class="lemma-summary" label-module="lemmaSummary">(.*?)<div class="configModuleBanner">'
        reg = r'</span></h2>(.*?)<h\d>'
        text = re.search(reg, text).group(1).replace("&nbsp;", " ").replace("&amp;", "&").replace('&gt;', '>') \
            .replace('&lt;', '<').replace('&#91;', '[').replace('&#93;', ']')
        # print text
        # return None
        regs = [r'<style>(.*?)</style>', r'<script>(.*?)</script>', r'<.*?>', r'\[\d+\]', r'【试听】', r'显示视频']
        for r in regs:
            search_result = re.search(r, text)
            while search_result:
                text = text.replace(search_result.group(0), "")
                search_result = re.search(r, text)
        print text
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
    reg = r'\d+\.(.*)(\.+.*)'
    result = re.match(reg, filename)
    if result:
        songname = result.group(1)
        postfix = result.group(2)
        keyword = songname.decode("gbk")
        print keyword
        # print type(keyword)
        Text = fetchText(keyword)
        if Text is None:
            print songname.decode("gbk") + "  ERROR"
            continue
        with open(os.path.join(dir_text, str(counter) + "." + songname + ".txt"), "w") as f:
            f.write(Text)
        shutil.move(os.path.join(dir_original, filename), os.path.join(dir_music, str(counter) + "." + songname + postfix))
        print songname.decode("gbk") + "  OK"
        counter += 1

