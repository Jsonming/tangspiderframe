# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from tangspiderframe.items import TangspiderframeItem


class TextSwitzerlandNzzContentSpider(RedisSpider):
    name = 'text_switzerland_nzz_content'
    allowed_domains = ['www.nzz.ch']
    start_urls = ['https://www.nzz.ch/international/china-japan-und-suedkorea-vereint-gegen-nordkorea-ld.1530641']
    redis_key = "text_switzerland_nzz_link"

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        title = response.xpath('//h1[@class="headline__title"]/text()').extract()
        content = response.xpath('//p/text()').extract()
        catagpory = response.url.split("/")[3]
        item = TangspiderframeItem()
        item['url'] = response.url
        item['title'] = " ".join(title)
        item['content'] = " ".join(content)
        item['category'] = catagpory
        yield item
