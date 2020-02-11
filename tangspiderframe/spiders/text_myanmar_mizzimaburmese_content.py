# -*- coding: utf-8 -*-
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider
# import myanmar
# from myanmar import converter


class TextMyanmarMizzimaburmeseContentSpider(RedisSpider):
    name = 'text_myanmar_mizzimaburmese_content'

    start_urls = ['https://www.abante.com.ph/schedule-sa-mga-bangko-karong-holiday-season.htm']
    redis_key = "text_myanmar_mizzimaburmese_link"



    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }


    def parse(self, response):
        title = response.xpath('//div[@class="news-details-title"]//text()').extract()
        content = response.xpath('//p/text()').extract()
        content = ''.join(content)
        content = content.replace("\n", "  ")
        content = content.replace("\t", "  ")
        content = myanmar.converter.convert(content,'unicode', 'zawgyi')
        item = TangspiderframeItem()
        item['url'] = response.url
        # item['category'] = response.url.split('/')[3]
        item['title'] = ''.join(title)
        item['content'] = content
        # print(item)
        yield item

