# -*- coding: utf-8 -*-
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider


class TextCanadaJournaldemontrealContentSpider(RedisSpider):
    name = 'text_canada_journaldemontreal_porte_content'
    start_urls = ['https://www.journaldemontreal.com/2019/12/23/le-conte-quebecois-du-loup-garou']
    redis_key = "text_canada_journaldemontreal_5_link"



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
        item['category'] = "5-minutes"
        item['title'] = ''.join(title)
        item['content'] = content
        # print(item)
        yield item
