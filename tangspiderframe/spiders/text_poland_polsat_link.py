# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextPolandPolsatLinkSpider(scrapy.Spider):
    name = 'text_poland_polsat_link'
    allowed_domains = ['www.polsat.pl/']

    def start_requests(self):
        for i in range(1,143):
            url="https://www.polsat.pl/newsy-ajax-asc_7768/module38328/page{i}/?_=1574911473758".format(i=i)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        links = response.xpath('//a[@class="iframe cboxElement"]/@href').extract()
        for link in links:
            item = TangspiderframeItem()
            item['url'] = link
            # print(item)
            yield item


