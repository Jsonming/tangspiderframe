# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextEnglishChinadailyLinkSpider(scrapy.Spider):
    name = 'text_english_chinadaily_link'
    allowed_domains = ['www.chinadaily.com.cn']
    start_urls = ['http://www.chinadaily.com.cn/world/asia_pacific/page_{}.html'.format(i) for i in range(1, 3000)]

    def parse(self, response):
        links = response.xpath('//a[@shape="rect"]/@href').extract()
        for link in links:
            url = "http:" + link
            item = TangspiderframeItem()
            item["url"] = url
            yield item
