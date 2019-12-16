# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider


class TextThaiDailynewsContentSpider(RedisSpider):
    name = 'text_thai_dailynews_agriculture_content'
    allowed_domains = ['www.dailynews.co.th']
    redis_key = "text_thai_dailynews_agriculture_link"

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        title_tag = response.xpath('//h1[@class="title"]/text()').extract()

        paragraph_tag = response.xpath(
            '//article[@id="news-article"]/section[@class="article-detail"]/div//text()').extract()
        paragraph = [item.strip() for item in paragraph_tag if "googletag" not in item and "Definitions" not in item]

        catagpory = response.url.split("/")[3]
        item = TangspiderframeItem()
        item['url'] = response.url
        item['title'] = title_tag[0].strip() if title_tag else ""
        item['content'] = " ".join(paragraph)
        item['category'] = catagpory
        yield item
