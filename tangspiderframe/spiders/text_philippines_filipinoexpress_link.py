# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextPhilippinesFilipinoexpressLinkSpider(scrapy.Spider):
    name = 'text_philippines_filipinoexpress_express_week_link'
    # handle_httpstatus_list = [404]
    # urls=["http://www.filipinoexpress.com/news", #100
    #       "http://www.filipinoexpress.com/business-economy",  #53
    #       "http://www.filipinoexpress.com/editorial-opinion", #46
    #       "http://www.filipinoexpress.com/entertainment", #52
    #       "http://www.filipinoexpress.com/express-week",  #31
    #       "http://www.filipinoexpress.com/sports", #34
    #       ""]

    def start_requests(self):
        for i in range(0,540,10):
            url = "http://www.filipinoexpress.com/sports?start={i}".format(i=i)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        links = response.xpath('//h2/a/@href').extract()
        for link in links:

            item = TangspiderframeItem()
            item['url'] = "http://www.filipinoexpress.com"+link
            # print(item)
            yield item



