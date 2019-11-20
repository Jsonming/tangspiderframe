# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextSpeechoceanLinkSpider(scrapy.Spider):
    name = 'text_speechocean_link'
    allowed_domains = ['www.speechocean.com']
    start_urls = ['http://www.speechocean.com/datacenter/recognition/{}.html?prosearch=#datacenter_do'.format(i) for i
                  in range(1, 5)]

    def parse(self, response):
        products = response.xpath('//div[@class="tit-list"]/div')

        for product in products:
            product_url = ''.join(product.xpath('.//a/@href').extract())
            item = TangspiderframeItem()
            item["url"] = product_url
            yield item
