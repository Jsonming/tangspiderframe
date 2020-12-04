# -*- coding: utf-8 -*-
import scrapy
import re
from tangspiderframe.items import TangspiderframeItem


class TextKoreaKidsLinkSpider(scrapy.Spider):
    name = 'text_korea_kids_link'
    allowed_domains = ['kids.hankooki.com']
    start_urls = [
        'http://kids.hankooki.com/community/wwwboardlist.php?tablename=opinionroom&mode=&code_type=&indexid=&cat=&menu=&report=&query=&ms=&or=&page={}&codenum='.format(i) for i in range(1, 136)
    ]

    def parse(self, response):
        hrefs = re.findall('<td ><a href=(.*?)>', response.text)
        for href in hrefs:
            url = "http://kids.hankooki.com/community/" + href
            item = TangspiderframeItem()
            item['url'] = url
            yield item
