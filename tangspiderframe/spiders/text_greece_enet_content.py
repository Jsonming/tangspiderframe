# -*- coding: utf-8 -*-
from tangspiderframe.items import TangspiderframeItem
from scrapy import FormRequest
import scrapy
from scrapy_redis.spiders import RedisSpider

class GreeceEnetContentSpider(RedisSpider):
    name = 'text_greece_enet_content'
    allowed_domains = ['www.enet.gr']
    start_urls = ['http://www.enet.gr/?i=issue.el.home&date=24/01/2010&id=124463']



    def parse(self, response):
        title = response.xpath('//h2[@class="page-title"]/text()').extract()
        content = response.xpath('//p/text()').extract()
        content = ''.join(content)
        content = content.replace("\n", "  ")
        content = content.replace("\t", "  ")
        item = TangspiderframeItem()
        item['url'] = response.url
        item['category'] = response.url.split('/')[-2]
        item['title'] = ''.join(title)
        item['content'] = content
        # print(item)
        yield item

