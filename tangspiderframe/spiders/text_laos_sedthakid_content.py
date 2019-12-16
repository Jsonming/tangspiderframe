# -*- coding: utf-8 -*-
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider

class TextLaosSedthakidContentSpider(RedisSpider):
    name = 'text_laos_sedthakid_content'
    allowed_domains = ['sedthakid.la']
    start_urls = ['https://sedthakid.la/%e0%ba%aa%e0%ba%b2%e0%ba%a7%e0%ba%87%e0%ba%b2%e0%ba%a1%e0%ba%ab%e0%ba%bc%e0%ba%a7%e0%ba%87%e0%ba%9e%e0%ba%b0%e0%ba%9a%e0%ba%b2%e0%ba%87-%e0%ba%84%e0%ba%a7%e0%bb%89%e0%ba%b2%e0%ba%95%e0%ba%b3%e0%bb%81/']
    redis_key = "text_laos_sedthakid_link"

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

        # item['category'] = response.url.split('/')[3]

        item['title'] = ''.join(title)
        item['content'] = content
        # print(item)
        yield item

