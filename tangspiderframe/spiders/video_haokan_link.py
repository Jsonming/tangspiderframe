# -*- coding: utf-8 -*-
import scrapy
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
            item = TangspiderframeItem()
            item['url'] = url
            # print(item)
            yield item

