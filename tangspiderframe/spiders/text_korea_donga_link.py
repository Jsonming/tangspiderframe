# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextKoreaDongaLinkSpider(scrapy.Spider):
    name = 'text_korea_donga_link'
    allowed_domains = ['kids.donga.com']
    start_urls = [
        # 'https://kids.donga.com/?ptype=article&psub=world&gbn=01'
        'https://kids.donga.com/?ptype=article&psub=world&gbn=02'
    ]

    def parse(self, response):
        links = response.xpath("//ul[@class='article']//dt[@class='at_title']/a/@href").extract()
        for link in links:
            item = TangspiderframeItem()
            item['url'] = link
            yield item
        a_link = response.xpath("//a[@class='pg_page pg_next']/@href").extract()
        if a_link:
            next_link = "https://kids.donga.com" + a_link[0].strip(".")
            yield scrapy.Request(next_link, callback=self.parse, dont_filter=False)
