# -*- coding: utf-8 -*-
import re
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextEnglishBingLocalSpider(scrapy.Spider):
    name = 'text_english_bing_local'
    allowed_domains = ['cn.bing.com']

    def start_requests(self):
        with open(r'C:\Users\Administrator\Desktop\words.txt', 'r', encoding='utf8')as f:
            for key_word in f:
                keyword = key_word.strip()
                url = "https://cn.bing.com/dict/search?q={keyword}&go=Search&qs=ds&form=Z9LH5".format(keyword=keyword)
                yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': keyword}, dont_filter=True)

    def parse(self, response):
        pron = {"uk": "", "us": ""}

        us = response.xpath('//div[@class="hd_p1_1"]/div[@class="hd_prUS"]/text()').extract()
        if us:
            pron["us"] = re.findall("\[(.*?)\]", "".join(us[0]))
        uk = response.xpath('//div[@class="hd_p1_1"]/div[@class="hd_pr"]/text()').extract()
        if uk:
            pron["uk"] = re.findall("\[(.*?)\]", "".join(uk[0]))

        item = TangspiderframeItem()
        item['keyword'] = response.meta.get("keyword")
        item["content"] = pron
        item["url"] = "https://cn.bing.com/dict/search?q={}&go=Search&qs=ds&form=Z9LH5".format(response.meta.get("keyword"))
        yield item
