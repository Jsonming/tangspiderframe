# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextChinaHaodfLinkSpider(scrapy.Spider):
    name = 'text_china_haodf_link'
    allowed_domains = ['www.haodf.com']
    start_urls = [
        'https://www.haodf.com/sitemap-zx/2020/',
        'https://www.haodf.com/sitemap-zx/2019/',
        'https://www.haodf.com/sitemap-zx/2018/',
        'https://www.haodf.com/sitemap-zx/2017/',
        'https://www.haodf.com/sitemap-zx/2016/',
        'https://www.haodf.com/sitemap-zx/2015/',
        'https://www.haodf.com/sitemap-zx/2014/',
        'https://www.haodf.com/sitemap-zx/2013/',
        'https://www.haodf.com/sitemap-zx/2012/',
        'https://www.haodf.com/sitemap-zx/2011/',
        'https://www.haodf.com/sitemap-zx/2010/',
    ]

    def parse(self, response):
        links = response.xpath('//div[@class="dis_article_2 clearfix"][2]//a/@href').extract()
        for link in links:
            url = "https:" + link
            yield scrapy.Request(url=url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        links = response.xpath('//li[@class="hh"]/a/@href').extract()
        for link in links:
            url = "https:" + link
            item = TangspiderframeItem()
            item['url'] = url
            yield item