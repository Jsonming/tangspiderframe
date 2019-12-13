# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextLaosKongthapLinkSpider(scrapy.Spider):
    name = 'text_laos_kongthap_link'
    allowed_domains = ['www.kongthap.gov.la']
    start_urls = ["http://www.kongthap.gov.la/index1.php?lang=lo&at=at&pg=1&h=active1"
    "http://www.kongthap.gov.la/index1.php?lang=lo&at=at&pg=2&i=active1"
    "http://www.kongthap.gov.la/index1.php?lang=lo&at=at&pg=2&j=active1"
    "http://www.kongthap.gov.la/index1.php?lang=lo&at=at&pg=2&k=active1"
    "http://www.kongthap.gov.la/index1.php?lang=lo&at=at&pg=2&l=active1"
    "http://www.kongthap.gov.la/index1.php?lang=lo&at=at&pg=2&m=active1"]


    def parse(self, response):
        next_links = response.xpath('//*[@id="listNewsLG"]/div[1]/center/b/nav/ul/li[-2]/a/@href').extract()
        for next_link in next_links:
            next_link = "http://www.kongthap.gov.la/index1.php"+next_link
            yield scrapy.Request(url=next_link, callback=self.parse, dont_filter=True)

        links = response.xpath('//div[@class="row"]//a//@href').extract()
        for pattern in links:
            link = "http://www.kongthap.gov.la/index1.php"+pattern

            item = TangspiderframeItem()
            item['url'] = link
            print(item)
            # yield item



