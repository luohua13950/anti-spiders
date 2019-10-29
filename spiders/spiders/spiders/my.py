# -*- coding: utf-8 -*-
import scrapy
import re
import urllib
import urllib.request
import time
import os
from fontTools.ttLib import TTFont


class MySpider(scrapy.Spider):
    name = 'my'
    allowed_domains = ['www.maoyan.com']
    start_urls = ['https://www.maoyan.com/board/1']
    base_font_dir = "..\\..\\data\\maoyan_data\\base.woff"
    data_dir = "..\\..\\data\\maoyan_data\\"

    def parse(self, response):
        print("开始冒烟")
        html = response.text
        dst_corresponding = self.operate_font(html)
        print(dst_corresponding)

    def operate_font(self, html):
        _font_url = re.findall(r"url\((.*?)\)", html)
        if _font_url:
            f_url = [url.replace("'", "").replace("'", "") for url in _font_url]
            font_url = ["https:" + url for url in f_url if url.endswith("woff")]
            filename = self.download_font_file(font_url)
            print(filename)
            if os.path.isfile(filename):
                print("下载字体文件结束")
                return self.get_font(filename)
            else:
                print("下载失败")
            return 0

    def download_font_file(self, font_url):
        if not font_url:
            return 0
        print("下载字体文件")
        filename = os.path.join(self.data_dir, font_url[0].split("/")[-1])
        font_ret = urllib.request.urlretrieve(font_url[0], filename=filename)
        return filename

    def get_font(self,filename):
        font_base = TTFont(self.base_font_dir)
        font = TTFont(filename)

        base_corresponding = {"uniEEC6": 6,
                              "uniE9F5": 2,
                              "uniF7EE": 7,
                              "uniECA8": 0,
                              "uniF0F0": 3,
                              "uniEA0A": 4,
                              "uniE96B": 5,
                              "uniF070": 9,
                              "uniECD1": 1,
                              "uniE99C": 8,
        }
        base_key = list(font_base["glyf"].keys())[2:]
        key = list(font["glyf"].keys())[2:]
        print(base_key)
        print(key)
        dst_corresponding = {}
        base_coordinates = {bk: list(font_base["glyf"][bk].coordinates) for bk in base_key}
        target_coordinates = {k: list(font["glyf"][k].coordinates) for k in key}
        for bk, b_coordinates in base_coordinates.items():
            for k, coordinates in target_coordinates.items():
                if self.cmp(b_coordinates, coordinates, bk, k):
                    dst_corresponding[k] = base_corresponding[bk]
                    print(k, ":", base_corresponding[bk])
                    continue
        return dst_corresponding

    def cmp(self, base, target, *args):
        base_len, target_len = len(base), len(target)
        if args:
            bk, k = args
        count = 0
        for bs in base:
            for tg in target:
                if abs(int(bs[0]) - int(tg[0])) < 20 and abs(int(bs[1]) - int(tg[1])) < 20:
                    count += 1
        # print(base_len,target_len,bk,k,count)
        return abs(count - base_len) < 5 or abs(count - target_len) < 5 or count > max([base_len, target_len])



