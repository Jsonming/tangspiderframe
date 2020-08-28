# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextChinaZidianContentSpider(scrapy.Spider):
    name = 'text_china_zidian_content'
    allowed_domains = ['zidian.miaochaxun.com']
    start_urls = ['http://zidian.miaochaxun.com/duoyinzi.html']

    def parse(self, response):
        item_li = response.xpath('//div[@class="mcon f14 bt"]/ul/li')
        for li in item_li:
            word = li.xpath("./a[1]/text()").extract()
            pronunciation = li.xpath("./a[2]/text()").extract()
            item = TangspiderframeItem()
            item['url'] = response.url
            item['title'] = word[0]
            item['content'] = pronunciation[0]
            yield item

        next_page = response.xpath('//a[contains(text(),  "下一页")]/@href').extract()
        if next_page:
            next_url = "http://zidian.miaochaxun.com/" + next_page[0]
            yield scrapy.Request(url=next_url, callback=self.parse, dont_filter=True)
