# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider


class TextChianGushi365ContentSpider(RedisSpider):
    name = 'text_chian_gushi365_content'
    allowed_domains = ['www.gushi365.com']
    start_urls = ['http://www.gushi365.com/info/7893.html']

    redis_key = "text_chian_gushi365_link"
    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        nav = response.xpath('//nav[@class="breadcrumb"]/a/text()').extract()
        category = "".join(nav).replace("首页", '')
        header_h = response.xpath('//h1/text()').extract()
        title = "".join(header_h)
        content_p = response.xpath('//div[@class="single-content"]//p//text()').extract()
        content = "".join([p.strip() for p in content_p])
        item = TangspiderframeItem()
        item['url'] = response.url
        item['category'] = category
        item['content'] = content
        item['title'] = title
        return item
