# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextPakistanExpressLinkSpider(scrapy.Spider):
    name = 'text_pakistan_express_science_link'
    handle_httpstatus_list = [404,429]
    # time.sleep()

    # urls = [
    #     'https://www.express.pk/sports/',
    #     'https://www.express.pk/saqafat/',
    #     'https://www.express.pk/weird-news/',
    #     'https://www.express.pk/health/',
    #     'https://www.express.pk/science/',
    #     'https://www.express.pk/business/',
    #     'https://www.express.pk/blog/',
    # ]

    def start_requests(self):
        for i in range(1,300):
            url = "https://www.express.pk/science/archives/?page={i}".format(i=i)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        links = response.xpath('//a[@class="image"]/@href').extract()
        for link in links:

            item = TangspiderframeItem()
            item['url'] = link
            # print(item)
            yield item



