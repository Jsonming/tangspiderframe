# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider


class TextChinaRuiwenContentSpider(RedisSpider):
    name = 'text_china_ruiwen_content'
    allowed_domains = ['www.ruiwen.com']
    start_urls = ['http://www.ruiwen.com/wenxue/tonghua/715791.html']

    redis_key = "text_china_ruiwen_link"
    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        title_h = response.xpath("//h1/text()").extract()
        title = "".join(title_h)
        content_p = response.xpath('//div[@class="content"]/p//text()').extract()
        content = "".join([p.strip() for p in content_p])
        item = TangspiderframeItem()
        item['url'] = response.url
        item['category'] = "童话"
        item['content'] = content
        item['title'] = title
        return item
