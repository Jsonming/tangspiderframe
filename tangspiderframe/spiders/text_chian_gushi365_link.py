# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextChianGushi365LinkSpider(scrapy.Spider):
    name = 'text_chian_gushi365_link'
    allowed_domains = ['www.gushi365.com']
    start_urls = ['http://www.gushi365.com/']

    def parse(self, response):
        link_href = response.xpath('//article//h2/a/@href').extract()
        for item in link_href:
            article_url = "http://www.gushi365.com" + item
            item = TangspiderframeItem()
            item['url'] = article_url
            yield item

        page = response.meta.get("page", 1)
        if page <= 195:
            url = "http://www.gushi365.com/digg/index_{}.html".format(page + 1)
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse, meta={"page": page + 1})
