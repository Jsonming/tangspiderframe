# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.common.common import md5
from tangspiderframe.items import TangspiderframeItem


class TextBingContentSpider(scrapy.Spider):
    name = 'text_bing_content'
    allowed_domains = ['cn.bing.com']
    start_urls = ['https://cn.bing.com/dict/service?q=key&offset=10&dtype=sen&&qs=n&form=Z9LH5&sp=-1&pq=key']

    def parse(self, response):
        lis = response.xpath('//div[@class="se_li"]')
        for li in lis:
            sen_en = li.xpath(".//div[@class='sen_en']//text()").extract()
            sentens = "".join(sen_en)
            md = md5(sentens)
            item = TangspiderframeItem()
            item['content'] = sentens
            item['title'] = response.meta.get("keyword")
            item['category'] = ''
            item['fingerprint'] = md
            yield item
