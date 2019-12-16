# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextLaosKongthapLinkSpider(scrapy.Spider):
    name = 'text_laos_kongthap_link'
    allowed_domains = ['www.kongthap.gov.la']

    def start_requests(self):
        for i in ["h","i","j","k","l","m"]:
            for j in range(1,153):
                url = "http://www.kongthap.gov.la/index1.php?lang=lo&at=at&pg={j}&{i}=active1".format(j=j,i=i)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)


    def parse(self, response):
        links = response.xpath('//*[@id="listNewsLG"]/div[1]/div[3]/div[contains(@class, "col-xs-")]/a/@href').extract()
        for pattern in links:
            link = "http://www.kongthap.gov.la/index1.php"+pattern

            item = TangspiderframeItem()
            item['url'] = link
            # print(item)
            yield item



