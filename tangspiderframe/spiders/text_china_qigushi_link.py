# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextChinaQigushiLinkSpider(scrapy.Spider):
    name = 'text_china_qigushi_link'
    allowed_domains = ['www.qigushi.com']
    start_urls = [
        # 'http://www.qigushi.com/tonghuagushi/',
        # 'http://www.qigushi.com/chengyugushi/',
        'http://www.qigushi.com/yuyangushi/',
        'http://www.qigushi.com/shenhuagushi/'
        'http://www.qigushi.com/gudaigushi/',

        'http://www.qigushi.com/shuiqian/',
        'http://www.qigushi.com/baobao/',
        'http://www.qigushi.com/zheligushi/',
        'http://www.qigushi.com/mingren/',
        'http://www.qigushi.com/1001/',
        'http://www.qigushi.com/gelin/',
        'http://www.qigushi.com/ats/',
        'http://www.qigushi.com/aiguogushi/',
    ]

    def parse(self, response):
        link_a = response.xpath('//div[@id="lieb"]/dl//h2/a/@href').extract()
        for item in link_a:
            article_url = item
            item = TangspiderframeItem()
            item['url'] = article_url
            yield item

        page = response.meta.get("page", 1)
        if page <= 51:
            url = "http://www.qigushi.com/tonghuagushi/index_{}.html".format(page + 1)
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse, meta={"page": page + 1})
