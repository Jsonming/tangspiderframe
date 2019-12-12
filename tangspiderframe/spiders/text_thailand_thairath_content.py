# -*- coding: utf-8 -*-
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider

class TextThailandThairathContentSpider(RedisSpider):
    name = 'text_thailand_thairath_content'
    allowed_domains = ['www.thairath.co.th']
    start_urls = ['https://www.thairath.co.th/news/royal/1724635']
    redis_key = "text_thailand_thairath_link"

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }



    def parse(self, response):
        title = response.xpath('//h1/text()').extract()
        content = response.xpath('//p/text()').extract()
        content = ''.join(content)
        content = content.replace("\n", "  ")
        content = content.replace("\t", "  ")
        item = TangspiderframeItem()
        item['url'] = response.url
        item['category'] = response.url.split('/')[3]
        item['title'] = ''.join(title)
        item['content'] = content
        # print(item)
        yield item

