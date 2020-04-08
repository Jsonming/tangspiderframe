# -*- coding: utf-8 -*-
import re
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextChinaChinadailyLinkSpider(scrapy.Spider):
    name = 'text_china_chinadaily_link'
    allowed_domains = ['cn.chinadaily.com.cn']
    start_urls = [
        'https://china.chinadaily.com.cn/5bd5639ca3101a87ca8ff636'
    ]

    def parse(self, response):
        links = response.xpath('//div[@class="busBox3"]//h3/a/@href').extract()
        for link in links:
            item = TangspiderframeItem()
            item['url'] = "https:" + link
            yield item

        page = re.search("page_(\d+).html", response.url)
        if page:
            next_page_num = int(page.group(1)) + 1
            next_page_url = re.sub("page_(\d+).html", "page_{}.html".format(next_page_num), response.url)
        else:
            next_page_url = response.url + "/page_2.html"

        yield scrapy.Request(url=next_page_url, dont_filter=True, callback=self.parse)
