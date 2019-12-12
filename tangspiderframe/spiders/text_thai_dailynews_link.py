# -*- coding: utf-8 -*-
import scrapy


class TextThaiDailynewsLinkSpider(scrapy.Spider):
    name = 'text_thai_dailynews_link'
    allowed_domains = ['www.dailynews.co.th']
    start_urls = ['https://www.dailynews.co.th/main']

    def parse(self, response):
        links = response.xpath("//article/a/@href").extract()
        for link in links:
            url = "https://www.dailynews.co.th" + link
            print('"' + url + '"' + ",")
