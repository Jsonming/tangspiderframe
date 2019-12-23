# -*- coding: utf-8 -*-
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider


class TextPhilippinesFilipinoexpressContentSpider(RedisSpider):
    name = 'text_philippines_filipinoexpress_content'
    start_urls = ['http://www.filipinoexpress.com/sports/3340-helping-strangers-can-help-teens-have-more-confidence']
    redis_key = "text_philippines_filipinoexpress_express_week_link"

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }


    def parse(self, response):
        title = response.xpath('//h2//text()').extract()
        content = response.xpath('//p//text()').extract()
        content = ''.join(content)
        content = content.replace("\n", "  ")
        content = content.replace("\t", "  ")
        item = TangspiderframeItem()
        item['url'] = response.url
        item['category'] = "sports"
        item['title'] = ''.join(title)
        item['content'] = content
        # print(item)
        yield item

