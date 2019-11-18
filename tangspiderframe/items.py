# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TangspiderframeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 框架需求信息
    spider_name = scrapy.Field()  # 爬虫名
    fingerprint = scrapy.Field()  # 标识本条数据唯一值

    # 公共类型信息
    category = scrapy.Field()  # 文本信息源分类的类别

    # 文本类信息
    content = scrapy.Field()  # 文本内容
    title = scrapy.Field()  # 文本信息标题

    # 图片信息
    image_urls = scrapy.Field()  # 这个图片的URL 类型:list
    images = scrapy.Field()  # 这个看源码是结果字段
