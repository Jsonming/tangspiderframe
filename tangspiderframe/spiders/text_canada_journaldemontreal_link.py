# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextCanadaJournaldemontrealLinkSpider(scrapy.Spider):
    name = 'text_canada_journaldemontreal_link'

    def start_requests(self):
        for year in range(2011,2019):
            for month in range(1,13):
                month = str(month).zfill(2)
                for day in range(1, 31):
                    day = str(day).zfill(2)
                    url = "https://www.journaldemontreal.com/actualite/faits-divers/archives/{year}/{month}/{day}".format(year=year,month=month,day=day)
                    yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        links = response.xpath('//article/a/@href').extract()
        for link in links:

            item = TangspiderframeItem()
            item['url'] = link
            # print(item)
            yield item



