# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextMyanmarMizzimaburmeseLinkSpider(scrapy.Spider):
    name = 'text_myanmar_mizzimaburmese_link'
    start_urls = ["http://www.mizzimaburmese.com/"]

    def parse(self, response):
        links = response.xpath('//ul[@class="menu clearfix"]/li/a/@href').extract()
        for pattern in links:
            if pattern is not "/" and pattern is not "/world-news":
                link = "http://www.mizzimaburmese.com" + pattern
                yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        # print(response.text)
        next_links = response.xpath('//li[(contains(@class, "pager-next even"))]/a/@href').extract()
        for next_link in next_links:
            next_link = "http://www.mizzimaburmese.com" + next_link
            yield scrapy.Request(url=next_link, callback=self.parse_url, dont_filter=True)

        links = response.xpath('//div[@class="news-category-small-image-image"]/a/@href').extract()
        for link in links:
            link = "http://www.mizzimaburmese.com" +link
            item = TangspiderframeItem()
            item['url'] = link
            yield item
