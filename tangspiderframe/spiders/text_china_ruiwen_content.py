# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider


class TextChinaRuiwenContentSpider(scrapy.Spider):
    name = 'text_china_ruiwen_content'
    allowed_domains = ['www.ruiwen.com']
    start_urls = ['https://www.ruiwen.com/wenxue/gushihui/']

    # redis_key = "text_china_ruiwen_link"
    # custom_settings = {
    #     'REDIS_HOST': '123.56.11.156',
    #     'REDIS_PORT': 8888,
    #     'REDIS_PARAMS': {
    #         'password': '',
    #         'db': 0
    #     },
    # }

    def parse(self, response):
        # title_h = response.xpath("//h1/text()").extract()
        # title = "".join(title_h)
        # content_p = response.xpath('//div[@class="content"]/p//text()').extract()
        # content = "".join([p.strip() for p in content_p])
        # item = TangspiderframeItem()
        # item['url'] = response.url
        # item['category'] = "童话"
        # item['content'] = content
        # item['title'] = title
        # return item

        # 抓取故事
        cats = response.xpath('//div[@class="list_lan col_box"]/ul/li/a')
        for cat in cats:
            cat_link = cat.xpath("./@href").extract()
            cat_url = "https://www.ruiwen.com" + cat_link[0]
            cat_content = cat.xpath("./text()").extract()[0]
            yield scrapy.Request(url=cat_url, callback=self.parse_itme, dont_filter=True, meta={"cat": cat_content})

    def parse_itme(self, response):
        article_p = response.xpath('//div[@class="content"]//p')
        title_index = []
        for i, p in enumerate(article_p):
            if p.xpath("./strong").extract():
                title_index.append(i)

        for s_index, i_item in enumerate(title_index):
            category = response.xpath("//h1/text()").extract()[0]
            title = article_p[i_item].xpath("./strong/text()").extract()[0]
            try:
                next_tile = title_index[s_index + 1]
                content_str = ["".join(item.xpath("./text()").extract()) for item in article_p[i_item:next_tile]]
            except Exception as e:
                content_str = ["".join(item.xpath("./text()").extract()) for item in article_p[i_item:]]

            item = TangspiderframeItem()
            item['url'] = response.url
            item['category'] = category
            item['content'] = "".join([item.strip() for item in content_str])
            item['title'] = title
            yield item
