# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextEnglishChinadailyLinkSpider(scrapy.Spider):
    name = 'text_english_chinadaily_link'
    allowed_domains = ['www.chinadaily.com.cn']
    start_urls = ['http://www.chinadaily.com.cn/business']

    def parse(self, response):
        links = response.xpath('//div[@class="topNav2_art"]/ul/li/a/@href').extract()
        for link in links:
            if "http" not in link:
                link = "http:" + link
                yield scrapy.Request(url=link, callback=self.parse_item, dont_filter=True)


    def parse_item(self, response):
        next_links = response.xpath('//div[@id="div_currpage"]/a[@class="pagestyle"]/@href').extract()
        for next_link in next_links:
            next_link = "http:" + next_link
            yield scrapy.Request(url=next_link, callback=self.parse_item, dont_filter=True)

        links = response.xpath('//h4/a[@shape="rect"]/@href').extract()
        for link in links:
            url = "http:" + link
            item = TangspiderframeItem()
            item["url"] = url
            yield item
