# -*- coding: utf-8 -*-
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider

class TextVietnamVovContentSpider(RedisSpider):
    name = 'text_vietnam_vov_content'
    allowed_domains = ['vov.vn']
    start_urls = ['https://vov.vn/vu-an/dang-xet-xu-hai-cuu-bo-truong-nguyen-bac-son-va-truong-minh-tuan-990313.vov']
    redis_key = "text_vietnam_vov_link"

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }



    def parse(self, response):
        title = response.xpath('//h2/text()').extract()
        content = response.xpath('//p//text()').extract()
        content = ''.join(content)
        content = content.replace("\n", "  ")
        content = content.replace("\t", "  ")
        item = TangspiderframeItem()
        item['url'] = response.url

        # item['category'] = response.url.split('/')[3]

        item['title'] = ''.join(title)
        item['content'] = content
        # print(item)
        yield item

