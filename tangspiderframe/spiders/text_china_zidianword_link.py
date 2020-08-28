# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextChinaZidianwordLinkSpider(scrapy.Spider):
    name = 'text_china_zidianword_link'
    allowed_domains = ['zidian.miaochaxun.com']
    start_urls = ['http://zidian.miaochaxun.com/duoyinzi.html']

    def parse(self, response):
        item_li = response.xpath('//div[@class="mcon f14 bt"]/ul/li')
        for li in item_li:
            word = li.xpath("./a[1]/text()").extract()
            word_page = li.xpath("./a[1]/@href").extract()
            if word_page:
                word_url = "http://zidian.miaochaxun.com" + word_page[0].lstrip(".")
                yield scrapy.Request(url=word_url, meta={"word": word[0]}, callback=self.parse_item, dont_filter=True)

        next_page = response.xpath('//a[contains(text(),  "下一页")]/@href').extract()
        if next_page:
            next_url = "http://zidian.miaochaxun.com/" + next_page[0]
            yield scrapy.Request(url=next_url, callback=self.parse, dont_filter=True)

    def parse_item(self, response):
        detailed_pages = response.xpath('//div[@class="fright"]/a[contains(text(), "更多")]/@href').extract()
        for page in detailed_pages:
            item = TangspiderframeItem()
            item['url'] = page
            yield item
