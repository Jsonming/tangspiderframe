# -*- coding: utf-8 -*-
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider
from scrapy import FormRequest


class TextPakistanExpressContentSpider(RedisSpider):
    name = 'text_pakistan_express_weird_content'
    # name = 'text_pakistan_express_saqafat_content'
    # name = 'text_pakistan_express_sports_content'
    # name = 'text_pakistan_express_health_content'
    # name = 'text_pakistan_express_science_content'
    # name = 'text_pakistan_express_business_content'
    # name = 'text_pakistan_express_blog_content'

    start_urls = ['https://www.express.pk/story/1807726/509']
    redis_key = "text_pakistan_express_weird_link"
    # redis_key = "text_pakistan_express_saqafat_link"
    # redis_key = "text_pakistan_express_sports_link"
    # redis_key = "text_pakistan_express_health_link"
    # redis_key = "text_pakistan_express_science_link"
    # redis_key = "text_pakistan_express_business_link"
    # redis_key = "text_pakistan_express_blog_link"


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
        "Cookie": "__cfduid=d9fddc639d8ee3e2b0d639bd838e733bf1577069947; __cfruid=7fec64cb7440b4011acfa0ef41fbb3c67c59984f-1577069947; _ga=GA1.2.2111830010.1577069954; _gid=GA1.2.262721250.1577069954; __asc=e5168a4716f30b1d2511e334048; __auc=e5168a4716f30b1d2511e334048; __gads=ID=38b78f1e97fc6627:T=1577069999:S=ALNI_MZpnJmw8E5kDzwSV-JYnf-1aR93jg; __atuvc=3%7C52; __atuvs=5e005e7674aa425c002; GED_PLAYLIST_ACTIVITY=W3sidSI6Ikt3S3MiLCJ0c2wiOjE1NzcwODQ2MDIsIm52IjowLCJ1cHQiOjE1NzcwODI5MzgsImx0IjoxNTc3MDgzNzk4fV0.; trc_cookie_storage=taboola%2520global%253Auser-id%3D4facf365-8ce7-4bcd-b341-44d87ea239b3-tuct4f9ec27",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "TE": "Trailers"
           }



    def make_requests_from_url(self, url):
        return FormRequest(url, dont_filter=True,headers=self.headers)

    def parse(self, response):
        title = response.xpath('//h1//text()').extract()
        content = response.xpath('//p//text()').extract()
        content = ''.join(content)
        content = content.replace("\n", "  ")
        content = content.replace("\t", "  ")
        item = TangspiderframeItem()
        item['url'] = response.url
        item['category'] = "weird-news"
        item['title'] = ''.join(title)
        item['content'] = content
        # print(item)
        yield item

