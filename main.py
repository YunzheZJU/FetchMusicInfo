# -*- coding: utf-8 -*-
import os
import re
import requests
import urllib


def fetchText(keyword):
    # print keyword
    # print type(keyword)
    keyword = keyword.encode("utf-8")
    # print keyword
    # print type(keyword)
    # print type("现在就决定你要爱我")
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
    if not re.search(reg, text) is None:
        print "Error in searching."
        return None
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


dir_music = os.path.join(os.path.abspath("."), "music")
dir_text = os.path.join(os.path.abspath("."), "text")
if not os.path.exists(dir_music):
    exit(0)
if not os.path.exists(dir_text):
    os.mkdir(dir_text)
fileList = os.listdir(dir_music)
for filename in fileList:
    # print filename
    # print type(filename)
    filename = filename.decode("gbk")
    # print filename
    # print type(filename)
    reg = r'\d+\.(.*?)\s*-\s*(.*?)(\s|\.|\(|\xa3\xa8)'
    keyword = re.match(reg, filename).group(2)
    # print keyword
    # print type(keyword)
    Text = fetchText(keyword)
    if Text is None:
        print filename + "  ERROR"
        continue
    with open(os.path.join(dir_text, filename.replace(".mp3", "") + ".txt"), "w") as f:
        f.write(Text)
    print filename + "  OK"

