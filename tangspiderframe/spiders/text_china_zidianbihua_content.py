# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextChinaZidianbihuaContentSpider(scrapy.Spider):
    name = 'text_china_zidianbihua_content'
    allowed_domains = ['zidian.miaochaxun.com']
    start_urls = [
        'http://zidian.miaochaxun.com/bihua_{}.html'.format(str(i)) for i in range(3, 52)
    ]

    def parse(self, response):
        zi_a = response.xpath('//p[@class="zi"]/a')
        for zi in zi_a:
            base_url = zi.xpath("./@href").extract()[0]
            word = zi.xpath("./text()").extract()[0]
            pron_span = zi.xpath("./span/text()").extract()
            item = TangspiderframeItem()
            item['url'] = response.url
            item['category'] = base_url
            if pron_span:
                item['title'] = pron_span[0]
            item['content'] = word
            yield item
