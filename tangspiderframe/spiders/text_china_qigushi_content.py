# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider


class TextChinaQigushiContentSpider(RedisSpider):
    name = 'text_china_qigushi_content'
    allowed_domains = ['www.qigushi.com']
    start_urls = ['http://www.qigushi.com/gelin/1064.html']

    redis_key = "text_china_qigushi_link"
    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        category = response.xpath('//div[@id="place"]/a[2]/text()').extract()[0]
        title = response.xpath('//div[@id="info"]/dl/h1/a/text()').extract()[0]
        content = response.xpath('//dl[@id="zi"]//p//text()').extract()
        item = TangspiderframeItem()
        item['url'] = response.url
        item['category'] = category
        item['content'] = "".join([item.strip() for item in content])
        item['title'] = title
        yield item
