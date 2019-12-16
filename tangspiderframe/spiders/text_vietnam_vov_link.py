# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextVietnamVovLinkSpider(scrapy.Spider):
    name = 'text_vietnam_vov_link'
    allowed_domains = ['vov.vn']
    start_urls = ['https://vov.vn/']

    def parse(self, response):
        links = response.xpath('//ul[@class="l-grid"]//li/a/@href').extract()
        for parrten in links:
            if "http" not in parrten and "chinh-tri" not in parrten:
                url = "https://vov.vn"+parrten
                yield scrapy.Request(url=url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        next_links = response.xpath('//a[@class="next"]/@href').extract()
        for next_link in next_links:
            next_link = "https://vov.vn" + next_link
            yield scrapy.Request(url=next_link, callback=self.parse_url, dont_filter=True)

        links = response.xpath('//a[@class="cms-link"]/@href').extract()
        for link in links:
            item = TangspiderframeItem()
            item['url'] = "https://vov.vn" + link
            print(item)
            # yield item




