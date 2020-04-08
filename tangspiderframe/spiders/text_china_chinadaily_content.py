# -*- coding: utf-8 -*-
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextChinaChinadailyContentSpider(scrapy.Spider):
    name = 'text_china_chinadaily_content'
    allowed_domains = ['cn.chinadaily.com.cn']
    start_urls = ['https://cn.chinadaily.com.cn/a/202004/07/WS5e8bdf0aa3107bb6b57ab205.html']

    def parse(self, response):
        category = response.xpath('//div[@class="dingtou"]/div[@class="da-bre"]/a[2]/text()').extract()
        title = response.xpath("//h1/text()").extract()  # 文章标题
        content = response.xpath('//div[@class="article"]/p//text()').extract()

        item = TangspiderframeItem()
        item['url'] = response.url
        item['category'] = "".join(category).replace(" > ", '').strip()
        item['content'] = "".join([item.strip() for item in content])
        item['title'] = "".join(title)
        yield item
        # print(item)
