# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider


class TextPolandPolsatContentSpider(RedisSpider):
    name = 'text_poland_polsat_content'
    allowed_domains = ['www.polsat.pl']
    start_urls = ['https://www.polsat.pl/news/2016-04-19/znane-blizniaki-w-hells-kitchen-o-kogo-chodzi_1503801/']

    redis_key = 'text_poland_polsat_link'

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }


    def parse(self, response):
        title = response.xpath('//h1/text()').extract()
        content = response.xpath('//p/text()').extract()
        last1_link = response.xpath('//p[last()]//@href').extract()
        last2_link = response.xpath('//p[last()-1]//@href').extract()
        # print("last1_link",last1_link,"last2_link",last2_link)
        content = ''.join(content)
        content = content.replace("\n", "  ")
        content = content.replace("\t", "  ")
        if last1_link and last2_link:
            last1_content = response.xpath('//p[last()]/text()').extract()
            last2_content = response.xpath('//p[last()-1]/text()').extract()
            last1_content = ''.join(last1_content)
            last2_content = ''.join(last2_content)
            content = content.replace(last1_content,"")
            content = content.replace(last2_content, "")
            # print("1111111",content)
        elif last1_link and not last2_link:
            last1_content = response.xpath('//p[last()]/text()').extract()
            last1_content = ''.join(last1_content)
            content = content.replace(last1_content,"")
            # print("222222", content)
        elif last2_link and not last1_link:
            last2_content = response.xpath('//p[last()-1]/text()').extract()
            last2_content = ''.join(last2_content)
            content = content.replace(last2_content, "")
            # print("333333333", content)
        else:
            content = content
            # print("4444444", content)

        item = TangspiderframeItem()
        item['url'] = response.url
        item['category'] = response.url.split('/')[3]
        item['title'] = ''.join(title)
        item['content'] = content
        # print(item)
        yield item

