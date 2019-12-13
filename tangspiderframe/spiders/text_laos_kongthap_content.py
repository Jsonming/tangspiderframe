# -*- coding: utf-8 -*-
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider

class TextLaosKongthapContentSpider(RedisSpider):
    name = 'text_laos_kongthap_content'
    allowed_domains = ['www.kongthap.gov.la']
    # start_urls = ['https://www.vientianemai.net/khao/23041.html']
    redis_key = "text_laos_kongthap_link"

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }



    def parse(self, response):
        title = response.xpath('//*[@id="headpageLG"]/div[1]/font[1]/b/text()').extract()
        content = response.xpath('//*[@id="headpageLG"]/div[1]/div/font/text()').extract()
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

