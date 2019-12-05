# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider


class TextEnglishBbcContentSpider(RedisSpider):
    name = 'text_english_bbc_content'
    allowed_domains = ['www.bbc.com']
    # start_urls = [
    #     'https://www.bbc.com/news/business-{}'.format(i) for i in range(50471282, 50471283)
    # ]

    redis_key = "text_english_bbc_link"

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        title = response.xpath('//div[@id="page"]//div/h1/text()').extract()
        content = response.xpath('//div[@class="story-body__inner"]//p/text()').extract()
        if content:
            content = " ".join(content)

        item = TangspiderframeItem()
        item['url'] = response.url
        item['category'] = "business"
        item['title'] = ''.join(title)
        item['content'] = content
        yield item
