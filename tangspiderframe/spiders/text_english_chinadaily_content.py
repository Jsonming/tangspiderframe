# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider


class TextEnglishChinadailyContentSpider(RedisSpider):
    name = 'text_english_chinadaily_content'
    allowed_domains = ['www.chinadaily.com.cn']
    start_urls = ['http://www.chinadaily.com.cn/a/201912/10/WS5dee72d9a310cf3e3557cf5c.html']
    redis_key = "text_english_chinadaily_link"

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        title = response.xpath("//h1/text()").extract()
        contents = response.xpath('//div[@id="Content"]/p//text()').extract()
        paragraph = [content for content in contents]
        item = TangspiderframeItem()
        item['url'] = response.url
        item['title'] = title[0].strip() if title else ""
        item['content'] = " ".join(paragraph)
        yield item
