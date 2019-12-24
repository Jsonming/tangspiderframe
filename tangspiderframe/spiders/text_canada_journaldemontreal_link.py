# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextCanadaJournaldemontrealLinkSpider(scrapy.Spider):
    name = 'text_canada_journaldemontreal_enquetes_link'
    # start_urls = ["https://www.journaldemontreal.com/"]

    #     urls=["""
    # https://www.journaldemontreal.com/actualite
    # https://www.journaldemontreal.com/spectacles
    # https://www.journaldemontreal.com/argent
    # https://www.journaldemontreal.com/auto
    # https://www.journaldemontreal.com/monde
    # https://www.journaldemontreal.com/jm
    # https://www.journaldemontreal.com/porte-monnaie
    # https://www.journaldemontreal.com/maison-extra
    # https://www.journaldemontreal.com/5-minutes
    # https://www.journaldemontreal.com/voyages
    # https://www.journaldemontreal.com/opinions
    # https://www.journaldemontreal.com/blogues
    # https://www.journaldemontreal.com/24heures"""]

    def start_requests(self):
        for year in range(2013, 2019):
            for month in range(1, 13):
                month = str(month).zfill(2)
                for day in range(1, 31):
                    day = str(day).zfill(2)
                    url = "https://www.journaldemontreal.com/enquetes/archives/{year}/{month}/{day}".format(
                        year=year, month=month, day=day)
                    yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        links = response.xpath('//article/a/@href').extract()
        for link in links:
            item = TangspiderframeItem()
            item['url'] = link
            # print(item)
            yield item




