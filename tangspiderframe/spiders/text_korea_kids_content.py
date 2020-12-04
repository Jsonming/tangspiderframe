# -*- coding: utf-8 -*-
import scrapy
import re
from lxml import etree
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider


class TextKoreaKidsContentSpider(RedisSpider):
    name = 'text_korea_kids_content'
    allowed_domains = ['kids.hankooki.com']
    start_urls = [
        'http://kids.hankooki.com/community/wwwboardview.php?tablename=opinionroom&mode=&code_type=&page=3&cat=&menu=&report=&query=&ms=&indexid=3437&no=0&re=&idx=3437'
    ]
    redis_key = "text_korea_kids_link"
    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        content = re.findall('<td colspan="12" style="padding:15px">(.*?)</td>', response.text, re.S)
        new_content = "<td>" + "".join(content) + "</td>"
        html = etree.HTML(new_content)
        res = html.xpath(".//text()")
        item = TangspiderframeItem()
        item['url'] = response.url
        item['content'] = "".join(res)
        return item