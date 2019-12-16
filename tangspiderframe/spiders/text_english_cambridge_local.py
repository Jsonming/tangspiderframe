# -*- coding: utf-8 -*-
import json
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextEnglishCambridgeLocalSpider(scrapy.Spider):
    name = 'text_english_cambridge_local'
    allowed_domains = ['dictionary.cambridge.org']
    start_urls = ['http://dictionary.cambridge.org/']

    def start_requests(self):
        with open(r"D:\datatang\tangspiderframe\tangspiderframe\files\words.txt", 'r', encoding='utf8')as f:
            for word in f:
                url = "https://dictionary.cambridge.org/dictionary/english/{}".format(word.strip())
                yield scrapy.Request(url=url, dont_filter=True, meta={"word": word.strip()})

    def parse(self, response):
        pron = {"uk": "", "us": ""}
        pron["uk"] = "".join(response.xpath(
            '//*[@id="page-content"]/div[2]/div/div[1]/div[2]/div/div[3]/div/div/div/div[2]/span[1]/span[@class="pron dpron"]/span//text()').extract())
        pron["us"] = "".join(response.xpath(
            '//*[@id="page-content"]/div[2]/div/div[1]/div[2]/div/div[3]/div/div/div/div[2]/span[2]/span[@class="pron dpron"]/span//text()').extract())

        item = TangspiderframeItem()
        item['keyword'] = response.meta.get("word")
        item["content"] = pron
        item["url"] = "https://dictionary.cambridge.org/dictionary/english/{}".format(response.meta.get("word"))
        yield item
