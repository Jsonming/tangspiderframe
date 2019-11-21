# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextVietnamVidictContentSpider(scrapy.Spider):
    name = 'text_vietnam_vdict_content'
    allowed_domains = ['www.vdict.co']
    start_urls = ['http://www.vdict.co/index.php?word=hello&dict=en_vi']

    def parse(self, response):
        content = response.text
        item = TangspiderframeItem()
        item["url"] = response.url
        item["content"] = content
        yield item
