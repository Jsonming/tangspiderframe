# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextChinaYifanLinkSpider(scrapy.Spider):
    name = 'text_china_yifan_link'
    allowed_domains = ['www.yifanfx.com']
    start_urls = [
        'http://www.yifanfx.com/ertongshuiqiangushi/',
        # 'http://www.yifanfx.com/jingdianertonggushi/',
        # 'http://www.yifanfx.com/ertonggushidaquan/',
        # 'http://www.yifanfx.com/gelintonghua/',

    ]

    def parse(self, response):
        link_a = response.xpath('//div[@class="list"]//li/a/@href').extract()
        for item in link_a:
            article_url = item
            item = TangspiderframeItem()
            item['url'] = article_url
            yield item

        page = response.meta.get("page", 1)
        if page <= 689:
            url = "http://www.yifanfx.com/ertongshuiqiangushi/list_1_{}.html".format(page + 1)
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse, meta={"page": page + 1})


