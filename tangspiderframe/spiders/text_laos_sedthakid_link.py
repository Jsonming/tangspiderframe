# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextLaosSedthakidLinkSpider(scrapy.Spider):
    name = 'text_laos_sedthakid_link'
    allowed_domains = ['sedthakid.la']
    start_urls = ['https://sedthakid.la/']

    def parse(self, response):
        links = response.xpath('//ul[@class="menu"]//li/a/@href').extract()
        for url in links:
            yield scrapy.Request(url=url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        next_links = response.xpath('//a[@class="nextpostslink"]/@href').extract()
        for next_link in next_links:
            yield scrapy.Request(url=next_link, callback=self.parse_url, dont_filter=True)

        links = response.xpath('//a[@class="more-link"]/@href').extract()
        for link in links:
            item = TangspiderframeItem()
            item['url'] = link
            # print(item)
            yield item




