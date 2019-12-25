# -*- coding: utf-8 -*-
import scrapy
import json
from tangspiderframe.items import TangspiderframeItem


class TextSwitzerlandNzzLinkSpider(scrapy.Spider):
    name = 'text_switzerland_nzz_link'
    allowed_domains = ['www.nzz.ch/neueste-artikel']
    start_urls = ['https://enrico.nzz-tech.ch/v2/newest-articles?product=nzz&limit=8&offset={}'.format(i) for i in
                  range(128, 10000, 8)]

    def parse(self, response):
        resp = json.loads(response.text)
        data = resp.get("data")
        links = [item.get("metadata", {}).get("url") for item in data]
        for link in links:
            item = TangspiderframeItem()
            item['url'] = link
            yield item
