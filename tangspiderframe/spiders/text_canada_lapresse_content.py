# -*- coding: utf-8 -*-
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider


class TextCanadaLapresseContentSpider(RedisSpider):
    name = 'text_canada_lapresse_content'

    start_urls = ['https://www.lapresse.ca/voyage/plein-air/201912/23/01-5254762-gants-ou-mitaines-.php']
    redis_key = "text_canada_lapresse_link"



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
        item['category'] = response.url.split('/')[3]
        item['title'] = ''.join(title)
        item['content'] = content
        # print(item)
        yield item

