# -*- coding: utf-8 -*-
import json
import re
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextEnglishCambridgeLocalSpider(scrapy.Spider):
    name = 'text_english_cambridge_local'
    allowed_domains = ['dictionary.cambridge.org']
    start_urls = ['http://dictionary.cambridge.org/']

    def start_requests(self):
        with open(r"D:\datatang\tangspiderframe\tangspiderframe\files\words.txt", 'r', encoding='utf8')as f:
            data = f.readlines()
            for word in data:
                url = "https://dictionary.cambridge.org/dictionary/english/{}".format(word.strip())
                yield scrapy.Request(url=url, dont_filter=True, meta={"word": word.strip()})

    def parse(self, response):
        pron = {"uk": "", "us": ""}
        header = response.xpath('//div[@class="pos-header dpos-h"]')
        if header:
            uk = header[0].xpath('./span[@class="uk dpron-i "]//span[@class="pron dpron"]//text()').extract()
            pron["uk"] = re.findall("/(.*?)/", "".join(uk))

            us = header[0].xpath('./span[@class="us dpron-i "]//span[@class="pron dpron"]//text()').extract()
            pron["us"] = re.findall("/(.*?)/", "".join(us))

        item = TangspiderframeItem()
        item['keyword'] = response.meta.get("word")
        item["content"] = pron
        item["url"] = "https://dictionary.cambridge.org/dictionary/english/{}".format(response.meta.get("word"))
        yield item
