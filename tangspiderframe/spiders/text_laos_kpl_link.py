# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextLaosKplLinkSpider(scrapy.Spider):
    name = 'text_laos_kpl_link'
    allowed_domains = ['kpl.gov.la']
    start_urls = ['http://kpl.gov.la/News.aspx?cat=3',
                  'http://kpl.gov.la/News.aspx?cat=4',
                  'http://kpl.gov.la/News.aspx?cat=5',
                  'http://kpl.gov.la/News.aspx?cat=18',
                  'http://kpl.gov.la/News.aspx?cat=26',
                  'http://kpl.gov.la/News.aspx?cat=19',
                  'http://kpl.gov.la/News.aspx?cat=20',
                  'http://kpl.gov.la/News.aspx?cat=25']

    def parse(self, response):
        next_links = response.xpath('//a[@class="page-link next"]/@href').extract()
        for next_link in next_links:
            next_link = "http://kpl.gov.la/"+next_link
            yield scrapy.Request(url=next_link, callback=self.parse, dont_filter=True)

        links = response.xpath('//div[@class="title-news"]/a//@href').extract()
        for pattern in links:
            link = "http://kpl.gov.la/"+pattern

            item = TangspiderframeItem()
            item['url'] = link
            # print(item)
            yield item



