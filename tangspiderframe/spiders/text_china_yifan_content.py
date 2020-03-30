# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider


class TextChinaYifanContentSpider(RedisSpider):
    name = 'text_china_yifan_content'
    allowed_domains = ['www.yifanfx.com']
    start_urls = [
        'http://www.yifanfx.com/gelintonghua/30536.html'
    ]
    redis_key = "text_china_yifan_link"

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        category = response.xpath('//div[@class="position"]/a[2]/text()').extract()[0]
        title = response.xpath('//div[@class="article"]/h1/text()').extract()[0]
        content = response.xpath('//div[@class="article"]/p//text()').extract()
        item = TangspiderframeItem()
        item['url'] = response.url
        item['category'] = category
        item['content'] = "".join([item.strip() for item in content])
        item['title'] = title
        yield item
