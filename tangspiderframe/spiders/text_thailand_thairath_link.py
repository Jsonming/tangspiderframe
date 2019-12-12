# -*- coding: utf-8 -*-
import scrapy
import json
from tangspiderframe.items import TangspiderframeItem


class TextThailandThairathLinkSpider(scrapy.Spider):
    name = 'text_thailand_thairath_link'
    allowed_domains = ['www.thairath.co.th']
    start_urls = ['https://www.thairath.co.th/home']

    def parse(self, response):
        links = response.xpath('//ul[@class="css-1ltqhy5 e8s9vs4"]/li/div/ul/li/a//@href').extract()
        for pattern in links:
            if "http" not in pattern:
                url = "https://www.thairath.co.th/loadmore&section={pattern}&ts=0?&limit=8".format(pattern=pattern)
                yield scrapy.Request(url=url, callback=self.parse_url, dont_filter=True,meta={"pattern":pattern})

    def parse_url(self, response):
        pattern = response.meta["pattern"]
        resp = json.loads(response.text)
        minTs = resp.get("minTs")
        next_link = "https://www.thairath.co.th/loadmore&section={pattern}&ts={minTs}?&limit=8".format(pattern=pattern,minTs=minTs)
        yield scrapy.Request(url=next_link, callback=self.parse_url, dont_filter=True, meta={"pattern": pattern})

        data = resp.get("items", [])

        for img in data:
            canonical = img.get("canonical")
            item = TangspiderframeItem()
            item['url'] = canonical
            # print(item)
            yield item



