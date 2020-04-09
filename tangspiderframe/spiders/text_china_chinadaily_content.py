# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider


class TextChinaChinadailyContentSpider(RedisSpider):
    name = 'text_china_chinadaily_content'
    allowed_domains = ['cn.chinadaily.com.cn']
    start_urls = [
        # 'http://www.gov.cn/xinwen/2016-12/31/content_5155227.htm',
        # "http://news.cctv.com/2017/01/05/ARTIaW8eFJj5Mp9Ivtkagfit170105.shtml",
        # "http://v.cyol.com/content/2017-01/06/content_15210331.htm",
        'http://qclz.youth.cn/znl/201701/t20170106_9015306.htm'

    ]

    redis_key = 'text_china_chinadaily_link'
    custom_settings = {
        'DOWNLOAD_DELAY': '0.1',
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        category = response.xpath('//div[@class="dingtou"]/div[@class="da-bre"]/a[2]/text()').extract()
        title = response.xpath("//h1/text()").extract()  # 文章标题
        contents, para = [], []
        contents.extend(response.xpath('//div[contains(@class, "article")]//p'))
        contents.extend(response.xpath('//div[contains(@class, "zhengwen")]//p'))
        contents.extend(response.xpath('//div[contains(@class, "c_body")]//p'))
        contents.extend(response.xpath('//div[contains(@class, "cnt_bd")]//p'))
        for item in contents:
            para.extend(item.xpath("./text()").extract())
            sub_tag = item.xpath(".//*")
            for sub in sub_tag:
                if sub.root.tag != "script":
                    para.extend(sub.xpath(".//text()").extract())

        item = TangspiderframeItem()
        item['url'] = response.url
        item['category'] = "".join(category).replace(" > ", '').strip()
        item['content'] = "".join([item.strip() for item in para])
        item['title'] = "".join(title).strip()
        yield item
