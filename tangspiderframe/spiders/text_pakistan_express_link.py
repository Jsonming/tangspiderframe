# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextPakistanExpressLinkSpider(scrapy.Spider):
    name = 'text_pakistan_express_link'
    # start_urls = [
    #               'https://www.express.pk/sports/archives/?page=1',
    #               'https://www.express.pk/saqafat/archives/?page=1',
    #               'https://www.express.pk/weird-news/archives/?page=1',
    #               'https://www.express.pk/health/archives/?page=1',
    #               'https://www.express.pk/science/archives/?page=1',
    #               'https://www.express.pk/business/archives/?page=1',
    #               'https://www.express.pk/videos/archives/?page=1',
    #               'https://www.express.pk/blog/archives/?page=1',
    #               ]

    # urls = [
    #     'https://www.express.pk/sports/',
    #     'https://www.express.pk/saqafat/',
    #     'https://www.express.pk/weird-news/',
    #     'https://www.express.pk/health/',
    #     'https://www.express.pk/science/',
    #     'https://www.express.pk/business/',
    #     'https://www.express.pk/videos/',
    #     'https://www.express.pk/blog/',
    # ]

    headers ={
"Host": "www.express.pk",
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
"Accept-Encoding": "gzip, deflate, br",
"Connection": "keep-alive",
"Cookie":"__cfduid=d9fddc639d8ee3e2b0d639bd838e733bf1577069947; __cfruid=7fec64cb7440b4011acfa0ef41fbb3c67c59984f-1577069947; _ga=GA1.2.2111830010.1577069954; _gid=GA1.2.262721250.1577069954; __asc=e5168a4716f30b1d2511e334048; __auc=e5168a4716f30b1d2511e334048; __gads=ID=38b78f1e97fc6627:T=1577069999:S=ALNI_MZpnJmw8E5kDzwSV-JYnf-1aR93jg",
"Upgrade-Insecure-Requests": "1",
"Cache-Control": "max-age=0",
"TE": "Trailers"}

    def start_requests(self):
        for i in range(1,300):
            url = "https://www.express.pk/sports/archives/?page={i}".format(i=i)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True,headers=self.headers)

    def parse(self, response):
        print(response.code)
        print(response.text)
        # links = response.xpath('//a[@class="image"]/@href').extract()
        # for link in links:
        #
        #     item = TangspiderframeItem()
        #     item['url'] = link
        #     print(item)
        #     # yield item



