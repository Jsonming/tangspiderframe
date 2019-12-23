# -*- coding: utf-8 -*-
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider

class TextPakistanExpressContentSpider(RedisSpider):
    name = 'text_pakistan_express_sports_content'
    start_urls = ['https://www.express.pk/story/1925342/16']
    redis_key = "text_pakistan_express_sports_link"

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }



    def parse(self, response):
        title = response.xpath('//h1//text()').extract()
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

