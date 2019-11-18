# -*- coding: utf-8 -*-
import scrapy


class TextVietnamVidictContentSpider(scrapy.Spider):
    name = 'text_vietnam_vdict_content'
    allowed_domains = ['www.vdict.co']
    start_urls = ['http://www.vdict.co/index.php?word=hello&dict=en_vi']

    def parse(self, response):
        print(response.text)
