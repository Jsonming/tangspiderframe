# -*- coding: utf-8 -*-
import scrapy
import json
from tangspiderframe.items import TangspiderframeItem


class TextLaosVientianemaiLinkSpider(scrapy.Spider):
    name = 'text_laos_vientianemai_link'
    allowed_domains = ['www.vientianemai.net']
    start_urls = ['https://www.vientianemai.net/site/column/1.html',
                  'https://www.vientianemai.net/site/column/2.html',
                  'https://www.vientianemai.net/site/column/3.html',
                  'https://www.vientianemai.net/site/column/10.html']

    def start_requests(self):
        for i in [1,2,3,10]:
            for j in range(1,600):
                url = 'https://www.vientianemai.net/site/column/{i}.html?page={j}'.format(i=i,j=j)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        links = response.xpath('//h4/a//@href').extract()
        for pattern in links:
            link = "https://www.vientianemai.net"+pattern


            item = TangspiderframeItem()
            item['url'] = link
            # print(item)
            yield item



