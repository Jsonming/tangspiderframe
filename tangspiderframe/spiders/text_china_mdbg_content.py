# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem
from tangspiderframe.common.db import SSDBCon


class TextChinaMdbgContentSpider(scrapy.Spider):
    name = 'text_china_mdbg_content'
    allowed_domains = ['www.mdbg.net']
    start_urls = ['https://www.mdbg.net/chinese/dictionary?page=chardict&cdcanoce=0&cdqchi=以高价']

    def start_requests(self):
        ssdb_con = SSDBCon().connection()
        for i in range(50000):
            item = ssdb_con.rpop("text_china_mdbg_link")
            if item:
                word = item.decode("utf8")
                url = "https://www.mdbg.net/chinese/dictionary?page=chardict&cdcanoce=0&cdqchi={}".format(word)
                yield scrapy.Request(url=url, callback=self.parse, meta={"word": word}, dont_filter=True)

    def parse(self, response):
        pinyin = response.xpath("//td[@class='resultswrap']//tbody/tr/td[@class='details'][4]//text()").extract()
        item = TangspiderframeItem()
        item['url'] = response.url
        item['title'] = response.meta.get("word")
        if pinyin:
            item['content'] = "|".join(pinyin)
        else:
            item["content"] = ""

        return item
