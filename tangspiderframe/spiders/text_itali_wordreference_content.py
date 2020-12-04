# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem
from tangspiderframe.common.db import SSDBCon


class TextItaliWordreferenceContentSpider(scrapy.Spider):
    name = 'text_itali_wordreference_content'
    allowed_domains = ['www.wordreference.com.']
    start_urls = ['https://www.wordreference.com/definizione/cavigliera']

    def start_requests(self):
        ssdb_con = SSDBCon().connection()
        for i in range(10):
            item = ssdb_con.rpop("text_itali_wordreference_link")
            if item:
                word = item.decode("utf8")
                url = "https://www.wordreference.com/definizione/{}".format(word)
                yield scrapy.Request(url=url, callback=self.parse, meta={"word": word}, dont_filter=True)

    def parse(self, response):
        res = response.xpath('//*[@id="pronWR"]/text()').extract()
        item = TangspiderframeItem()
        item['url'] = response.url
        item['title'] = response.meta.get("word")
        if res:
            item['content'] = res[0]
        else:
            item["content"] = ""

        return item
