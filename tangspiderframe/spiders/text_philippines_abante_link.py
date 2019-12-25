# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextPhilippinesAbanteLinkSpider(scrapy.Spider):
    name = 'text_philippines_abante_link'
    start_urls = ["https://www.abante.com.ph/"]

    def parse(self, response):
        links = response.xpath('//ul[@class="main-menu menu bsm-pure clearfix"]/li/a/@href').extract()
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        next_links = response.xpath('//a[@class="next page-numbers"]/@href').extract()
        for next_link in next_links:
            yield scrapy.Request(url=next_link, callback=self.parse_url, dont_filter=True)

        links = response.xpath('//h2/a[@class="post-title post-url"]/@href').extract()
        for link in links:
            item = TangspiderframeItem()
            item['url'] = link
            yield item
