# -*- coding: utf-8 -*-
import scrapy


class TextChinaPageContentSpider(scrapy.Spider):
    name = 'text_china_page_content'
    allowed_domains = ['ecp.sgcc.com.cn']
    start_urls = ['http://ecp.sgcc.com.cn/']

    def parse(self, response):
        pass
