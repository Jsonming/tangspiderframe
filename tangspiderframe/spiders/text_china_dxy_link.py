# -*- coding: utf-8 -*-
import scrapy
import json
import re
from tangspiderframe.items import TangspiderframeItem


class TextChinaDxyLinkSpider(scrapy.Spider):
    name = 'text_china_dxy_link'
    allowed_domains = ['ask.dxy.com']

    def __init__(self, category=None, *args, **kwargs):
        super(TextChinaDxyLinkSpider, self).__init__(*args, **kwargs)

        self.start_urls = [
            'https://ask.dxy.com/view/i/question/list/section?section_group_name=buxian&page_index={}'.format(i)
            for i in range(int(category), int(category) + 30)]

    def parse(self, response):
        print(response.text)
        data = json.loads(response.text)
        items = data.get("data").get("items")
        for item in items:
            q_id = item.get("question", {}).get("id")
            url = "https://ask.dxy.com/question/{}".format(q_id)
            item = TangspiderframeItem()
            item['url'] = url
            yield item
