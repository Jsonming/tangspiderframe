# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider


class TextEnglishChinadailyContentSpider(scrapy.Spider):
    name = 'text_english_chinadaily_content'
    allowed_domains = ['www.chinadaily.com.cn']
    # start_urls = ['http://www.chinadaily.com.cn/a/201912/10/WS5dee72d9a310cf3e3557cf5c.html']
    # redis_key = "text_english_chinadaily_link"
    #
    # custom_settings = {
    #     'REDIS_HOST': '123.56.11.156',
    #     'REDIS_PORT': 8888,
    #     'REDIS_PARAMS': {
    #         'password': '',
    #         'db': 0
    #     },
    # }
    #
    # def parse(self, response):
    #     title = response.xpath("//h1/text()").extract()
    #     contents = response.xpath('//div[@id="Content"]/p//text()').extract()
    #     paragraph = [content for content in contents]
    #     item = TangspiderframeItem()
    #     item['url'] = response.url
    #     item['title'] = title[0].strip() if title else ""
    #     item['content'] = " ".join(paragraph)
    #     yield item

    start_urls = ['http://www.chinadaily.com.cn/']

    def parse(self, response):
        links = response.xpath('//ul[@class="dropdown"]/li[position()>3]/a/@href').extract()
        for link in links:
            if "http" not in link and "javascript:void(0);" not in link:
                link = "http:" + link
                category = link.split("/")[-1]
                yield scrapy.Request(url=link, callback=self.parse_link, dont_filter=True,meta={"category":category})

    def parse_link(self, response):
        category = response.meta["category"]
        links = response.xpath('//div[@class="topNav2_art"]/ul/li/a/@href').extract()
        for link in links:
            if "http" not in link:
                link = "http:" + link
                yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True,meta={"category":category})

    def parse_url(self, response):
        category = response.meta["category"]
        next_links = response.xpath('//div[@id="div_currpage"]/a[@class="pagestyle"]/@href').extract()
        for next_link in next_links:
            next_link = "http:" + next_link
            yield scrapy.Request(url=next_link, callback=self.parse_url, dont_filter=True,meta={"category":category})

        links = response.xpath('//h4/a[@shape="rect"]/@href').extract()
        for link in links:
            url = "http:" + link
            yield scrapy.Request(url=url, callback=self.parse_content, dont_filter=True,meta={"category":category})

    def parse_content(self, response):
        category = response.meta["category"]
        title = response.xpath("//h1/text()").extract()
        contents = response.xpath('//div[@id="Content"]/p//text()').extract()
        paragraph = [content for content in contents]
        item = TangspiderframeItem()
        item['category'] = category
        item['url'] = response.url
        item['title'] = title[0].strip() if title else ""
        item['content'] = " ".join(paragraph)
        yield item

