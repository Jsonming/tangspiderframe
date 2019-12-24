# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextCanadaLapresseLinkSpider(scrapy.Spider):
    name = 'text_canada_lapresse_link'
    start_urls = ["https://www.lapresse.ca/"]

    def parse(self, response):
        links = response.xpath('//nav/a/@href').extract()
        for pattern in links:
            link = "https://www.lapresse.ca"+pattern
            yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)



    def parse_url(self, response):
        links = response.xpath('//ul[@class="mainNav__subSections"]/li/a/@href').extract()
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_item, dont_filter=True)




    def parse_item(self, response):
        links = response.xpath('//article/a/@href').extract()
        for link in links:
            item = TangspiderframeItem()
            item['url'] = link
            # print(item)
            yield item



