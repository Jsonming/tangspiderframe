# -*- coding: utf-8 -*-
import scrapy
import time
import requests
import json
import re
import urllib
from urllib import parse
from scrapy.spiders import CrawlSpider, Rule, Request
from tangspiderframe.items import TangspiderframeItem
from scrapy.http.cookies import CookieJar

class VideoWeiboLinkSpider(scrapy.Spider):
    name = 'video_weibo_link'
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "pragma": "no-cache",
        "sec-fetch-mode": "navigate",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        "sec-fetch-site": "none",
        "cookie": "SUB=_2AkMruX5Jf8NxqwJRmPoVxG7ka4l3yg7EieKd5Y-SJRMxHRl-yT9jqlwjtRB6ADlQpwU6MYjzKJ7Kqyb0LFLnkJNsBNgj; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWg20.RBHqipo9qTM2D_rC5; SINAGLOBAL=8696952143569.81.1558573436947; _ga=GA1.2.1066465571.1565058895; __gads=ID=3955d0108686b954:T=1565058897:S=ALNI_Mb4b0_xXuYr00umBBUIoICwP0wEpg; UOR=,,news.sweden.cn; ULV=1575947928312:20:1:1:7166641179238.531.1575947927694:1574996499470"

    }
    # start_urls = "https://www.weibo.com/video/second?curr_tab=channel&type=icon&second_level_channel_id=4379553112491547&first_level_channel_id=4379553112491541&first_level_channel_name=时尚美妆&page_title=美妆教程"

    # def start_requests(self):
    #     session = requests.session()
    #     url = "https://www.weibo.com/video/second?curr_tab=channel&type=icon&second_level_channel_id=4379553112491547&first_level_channel_id=4379553112491541&first_level_channel_name=时尚美妆&page_title=美妆教程"
    #     response1 = session.get(url=url, headers=self.header)
    #     page_url = "https://www.weibo.com/video/aj/second?ajwvr=6&type=icon&second_level_channel_id=4379553112491547&editor_recommend_id=&since_id=4451165799120907&__rnd=1576742798962"
    #     response2 = session.get(url=page_url, headers=self.header)
    #     # print(response2.content.decode('gbk'))
    #     resp = json.loads(response2.text)
    #     data = resp.get("data")
    #     reg1 = 'video&.*?=http%3A%2F%2Ff.video.weibocdn.com%2F(.*?)&.*?=&qType=.*?0'
    #
    #     patterns = re.findall(reg1, data)
    #     for pattern in patterns:
    #         pattern = urllib.parse.unquote(pattern)
    #         link = "http://f.video.weibocdn.com/" + pattern
    #         item = TangspiderframeItem()
    #         item['url'] = link
    #         # print(item)
    #         yield item
    #
    #     reg2 = 'since_id=(.*?)\\">'
    #     since_ids = re.findall(reg2, data)
    #
    #     for since_id in since_ids:
    #         next_link = "https://www.weibo.com/video/aj/second?ajwvr=6&type=icon&second_level_channel_id=4379553112491547&editor_recommend_id=&since_id={since_id}&__rnd=1576742798962".format(
    #             since_id=since_id)
    #         yield scrapy.Request(url=next_link, callback=self.start_requests, dont_filter=True)

    # def parse(self, response):
    #     session = requests.session()
    #     page_url = "https://www.weibo.com/video/aj/second?ajwvr=6&type=icon&second_level_channel_id=4379553112491547&editor_recommend_id=&since_id=4451165799120907&__rnd=1576742798962"
    #     response = session.get(url=page_url, headers=self.header)
    #     print(response.content.decode('gbk'))
        # resp = json.loads(response.text)
        # data = resp.get("data")
        # reg1 = 'video&.*?=http%3A%2F%2Ff.video.weibocdn.com%2F(.*?)&.*?=&qType=.*?0'
        #
        # patterns = re.findall(reg1, data)
        # for pattern in patterns:
        #     pattern = urllib.parse.unquote(pattern)
        #     link = "http://f.video.weibocdn.com/" + pattern
        #     item = TangspiderframeItem()
        #     item['url'] = link
        #     # print(item)
        #     yield item
        #
        # reg2 = 'since_id=(.*?)\\">'
        # since_ids = re.findall(reg2, data)
        #
        # for since_id in since_ids:
        #     next_link = "https://www.weibo.com/video/aj/second?ajwvr=6&type=icon&second_level_channel_id=4379553112491547&editor_recommend_id=&since_id={since_id}&__rnd=1576742798962".format(
        #         since_id=since_id)
        #     yield scrapy.Request(url=next_link, callback=self.start_requests, dont_filter=True)

    # start_urls = ["https://www.weibo.com/"]

    # start_urls = ["https://www.weibo.com/video/aj/second?ajwvr=6&type=icon&second_level_channel_id=4379553112491547&editor_recommend_id=&since_id=4451165799120907&__rnd=1576742798962"
# ]
    def start_requests(self):
        session = requests.session()
        start_url = "https://www.weibo.com/video/second?curr_tab=channel&type=icon&second_level_channel_id=4379553112491547&first_level_channel_id=4379553112491541&first_level_channel_name=时尚美妆&page_title=美妆教程"
        response1 = session.get(url=start_url, headers=self.header)
        page_url = "https://www.weibo.com/video/aj/second?ajwvr=6&type=icon&second_level_channel_id=4379553112491547&editor_recommend_id=&since_id=4451165799120907&__rnd=1576742798962"
        response2 = session.get(url=page_url, headers=self.header)
        # print(response2.content.decode('gbk'))

        resp = json.loads(response2.text)
        data = resp.get("data")
        # reg1 = 'video&.*?=http%3A%2F%2Ff.video.weibocdn.com%2F(.*?)&.*?=&qType=.*?0'
        #
        # patterns = re.findall(reg1, data)
        # for pattern in patterns:
        #     pattern = urllib.parse.unquote(pattern)
        #     link = "http://f.video.weibocdn.com/" + pattern
        #     item = TangspiderframeItem()
        #     item['url'] = link
        #     # print(item)
        #     yield item
        reg2 = 'since_id=(.*?)\\">'
        since_ids = re.findall(reg2, data)
        for since_id in since_ids:
            next_link = "https://www.weibo.com/video/aj/second?ajwvr=6&type=icon&second_level_channel_id=4379553112491547&editor_recommend_id=&since_id={since_id}&__rnd=1576742798962".format(since_id=since_id)
            yield scrapy.Request(url=next_link, callback=self.parse,dont_filter=True,meta={"next_link":next_link})

    def parse(self,response):
        # print("response.url",response.text)
        url = response.meta["next_link"]
        session = requests.session()
        start_url = "https://www.weibo.com/video/second?curr_tab=channel&type=icon&second_level_channel_id=4379553112491547&first_level_channel_id=4379553112491541&first_level_channel_name=时尚美妆&page_title=美妆教程"
        response1 = session.get(url=start_url, headers=self.header)
        response2 = session.get(url=url, headers=self.header)
        # print(type(url),"url  ",url)
        # print(response2.content.decode('gbk'))
        response2 = session.get(url=url, headers=self.header)
        # print(response2.content.decode('gbk'))

        cookie = requests.utils.dict_from_cookiejar(response2.cookies)
        resp = json.loads(response2.text)
        data = resp.get("data")
        reg1 = 'video&.*?=http%3A%2F%2Ff.video.weibocdn.com%2F(.*?)&.*?=&qType=.*?0'

        patterns = re.findall(reg1, data)
        for pattern in patterns:
            pattern = urllib.parse.unquote(pattern)
            link = "http://f.video.weibocdn.com/" + pattern
            item = TangspiderframeItem()
            item['url'] = link
            # print(item)
            yield item

        reg2 = 'since_id=(.*?)\\">'
        since_ids = re.findall(reg2, data)

        for since_id in since_ids:
            next_link = "https://www.weibo.com/video/aj/second?ajwvr=6&type=icon&second_level_channel_id=4379553112491547&editor_recommend_id=&since_id={since_id}&__rnd=1576742798962".format(since_id=since_id)
            yield scrapy.Request(url=url, callback=self.parse,cookies=cookie, dont_filter=True,meta={"next_link":next_link})

