# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider


class TextChinaZidianwordContentSpider(RedisSpider):
    name = 'text_china_zidianword_content'
    allowed_domains = ['zidian.miaochaxun.com/duoyinzi.html']
    start_urls = ['http://chengyu.miaochaxun.com/zuci_Azqd66xGde7g.html']

    redis_key = "text_china_zidianword_link"
    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        "DOWNLOAD_DELAY": 4,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        word = response.xpath("//h2/text()").extract()[0].replace("的成语", "").replace("的组词", "")
        url = response.url
        if "com/zi" in url:
            item_li = response.xpath('//div[@class="mcon f14"]/ul/li')
            for li in item_li:
                phrase = li.xpath("./a[1]/text()").extract()
                pronunciation = li.xpath("./a[2]/text()").extract()
                item = TangspiderframeItem()
                item['url'] = response.url
                item['category'] = word
                item['title'] = pronunciation[0].strip()
                item['content'] = phrase[0]
                yield item
            next_page = response.xpath('//a[contains(text(),  "下一页")]/@href').extract()
            if next_page:
                next_url = "http://zuci.miaochaxun.com/" + next_page[0]
                yield scrapy.Request(url=next_url, meta={"word": response.meta.get("word")}, callback=self.parse,
                                     dont_filter=True)

        if "com/zuci" in url:
            item_li = response.xpath('//div[@class="mcon bt"]/ul/li')
            for li in item_li:
                phrase = li.xpath("./a[1]/text()").extract()
                item = TangspiderframeItem()
                item['url'] = response.url
                item['category'] = word
                item['content'] = phrase[0]
                yield item

            next_page = response.xpath('//a[contains(text(),  "下一页")]/@href').extract()
            if next_page:
                next_url = "http://chengyu.miaochaxun.com/" + next_page[0]
                yield scrapy.Request(url=next_url, meta={"word": response.meta.get("word")}, callback=self.parse,
                                     dont_filter=True)
