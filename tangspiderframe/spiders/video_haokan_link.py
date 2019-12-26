# -*- coding: utf-8 -*-
import scrapy
import os
import youtube_dl
import shutil
import json
import time
from tangspiderframe.items import TangspiderframeItem

class VideoHaoKanLinkSpider(scrapy.Spider):
    name = 'video_haokan1_link'

    # def start_requests(self):
    #     for pn in range(2,5):
    #         # url = "https://haokan.baidu.com/videoui/page/pc/search?pn={pn}&rn=10&_format=json&tab=video&query=%E5%8C%96%E5%A6%86".format(pn=pn)
    #         url = "https://haokan.baidu.com/videoui/page/pc/search?pn={pn}&rn=10&_format=json&tab=video&query=%E5%8C%96%E5%A6%86"
    #         yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
    #
    # def parse(self, response):
    #     resp = json.loads(response.text)
    #     data = resp.get("data")
    #     url_lists = data["response"]["list"]
    #     for url_list in url_lists:
    #         url = url_list["url"]
    #         if url:
    #             yield scrapy.Request(url=url, callback=self.parse_url, dont_filter=True)
    #
    # def parse_url(self, response):
    #     links = response.xpath('//video/@src').extract()
    #     for link in links:
    #         item = TangspiderframeItem()
    #         item['url'] = link
    #         # print(item)
    #         yield item
    def download(self,youtube_url):
        ydl_opts = {
            # outtmpl 格式化下载后的文件名，避免默认文件名太长无法保存
            'outtmpl': '%(id)s%(ext)s'
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
            path = os.getcwd()
            for file in os.listdir(path):
                if file.endswith("mp4"):
                    shutil.move(path + "/" + file, "/data/haokan" + "/" + file)


    def start_requests(self):
        for i in range(0,100):
            timestamp = int(round(time.time() * 1000))
            url = "https://haokan.baidu.com/videoui/api/videorec?tab=shishang&act=pcFeed&pd=pc&num=20&shuaxin_id={timestamp}".format(timestamp=timestamp)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        resp = json.loads(response.text)
        data = resp.get("data")
        url_lists = data["response"]["videos"]
        for url_list in url_lists:
            url = url_list["play_url"]
            self.youtube_url = url
            self.download(self.youtube_url)
            item = TangspiderframeItem()
            item['url'] = url
            # print(item)
            yield item

