# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextChinaRuiwenLinkSpider(scrapy.Spider):
    name = 'text_china_ruiwen_link'
    allowed_domains = ['www.ruiwen.com']
    start_urls = ['http://www.ruiwen.com/wenxue/tonghua/']

    def parse(self, response):
        article_link = response.xpath('//div[@class="list_news"]//h2/a/@href').extract()
        for item in article_link:
            article_url = "http://www.ruiwen.com" + item
            item = TangspiderframeItem()
            item['url'] = article_url
            yield item

        page = response.meta.get("page", 1)
        if page <= 10:
            url = "http://www.ruiwen.com/wenxue/tonghua/list_{}.html".format(page + 1)
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse, meta={"page": page + 1})
