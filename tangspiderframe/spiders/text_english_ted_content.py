# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider


class TextEnglishTedContentSpider(RedisSpider):
    name = 'text_english_ted_content'
    allowed_domains = ['www.ted.com']
    start_urls = ['https://www.ted.com/talks/sir_ken_robinson_do_schools_kill_creativity/transcript?language=en']
    redis_key = "text_english_ted_link"

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        paragraph = []
        contents = response.xpath('//p//text()').extract()
        for content in contents:
            text = content.replace('\t', '').replace("\n", " ")
            text = text.replace("(Laughter)", "").replace("(Applause)", "").strip()
            paragraph.append(text)

        item = TangspiderframeItem()
        item['url'] = response.url
        item['title'] = ' '.join(response.url.split("/")[4].split("_"))
        item['content'] = " ".join(paragraph)
        yield item
