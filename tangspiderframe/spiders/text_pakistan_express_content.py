# -*- coding: utf-8 -*-
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider
from scrapy import FormRequest
from lxml import etree
import requests
import scrapy


class TextPakistanExpressContentSpider(RedisSpider):
    name = 'text_pakistan_express_saqafat_content'
    handle_httpstatus_list = [429,301]

    start_urls = ['https://www.express.pk/story/1807726/509']
    redis_key = "text_pakistan_express_saqafat_link"

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    headers = {
        "Host": "www.express.pk",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cookie": "__cfduid=d9fddc639d8ee3e2b0d639bd838e733bf1577069947; _ga=GA1.2.2111830010.1577069954; _gid=GA1.2.262721250.1577069954; __auc=e5168a4716f30b1d2511e334048; __gads=ID=38b78f1e97fc6627:T=1577069999:S=ALNI_MZpnJmw8E5kDzwSV-JYnf-1aR93jg; __atuvc=4%7C52; trc_cookie_storage=taboola%2520global%253Auser-id%3D4facf365-8ce7-4bcd-b341-44d87ea239b3-tuct4f9ec27; __cfruid=765010dbaeceea08e8241d8c0d6733f0c9bb9987-1577152124; __asc=96976f0c16f35979435c93e03bc; _gat_gtag_UA_34505674_1=1",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "TE": "Trailers"
           }


    # def make_requests_from_url(self, url):
    #     return FormRequest(url, dont_filter=True,headers=self.headers)
    #
    # def parse(self, response):
    #     title = response.xpath('//h1//text()').extract()
    #     content = response.xpath('//p//text()').extract()
    #     content = ''.join(content)
    #     content = content.replace("\n", "  ")
    #     content = content.replace("\t", "  ")
    #     item = TangspiderframeItem()
    #     item['url'] = response.url
    #     item['category'] = "sports"
    #     item['title'] = ''.join(title)
    #     item['content'] = content
    #     # print(item)
    #     yield item


    def parse(self,response):
        session = requests.session()
        start_url = "https://www.express.pk/story/1807726/509"
        response1 = session.get(url=start_url, headers=self.headers)
        url = response.url
        response2 = session.get(url=url, headers=self.headers)
        html = etree.HTML(response2.text)

        title = html.xpath('//h1//text()')
        contents = html.xpath('//p//text()')
        content = ''.join(contents)
        content = content.replace("\n", "  ")
        content = content.replace("\t", "  ")
        item = TangspiderframeItem()
        item['url'] = response.url
        item['category'] = "saqafat"
        item['title'] = title[0]
        item['content'] = content
        # print(item)
        yield item





