# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextEnglishTedLinkSpider(scrapy.Spider):
    name = 'text_english_ted_link'
    allowed_domains = ['www.ted.com']
    start_urls = ['https://www.ted.com/talks?language=en&page={}&sort=newest'.format(i) for i in range(6, 106)]

    def parse(self, response):
        link_arg = response.xpath('//a[@class=" ga-link"]/@href').extract()
        for link in link_arg:
            url = "https://www.ted.com" + link
            head_url, language = url.split("?")
            item = TangspiderframeItem()
            item['url'] = head_url + "/transcript" + "?" + language
            yield item
