# -*- coding: utf-8 -*-
import scrapy
import re
from tangspiderframe.items import ImgsItem


class ImageCarSpider(scrapy.Spider):
    name = 'image_car'
    start_urls = ["https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=2%20&brandId=5%20&fctId=0%20&seriesId=0"]


    def __init__(self, *args, **kwargs):
        super(ImageCarSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        img_urls = response.xpath('//ul/li/h3//a/@href').extract()
        # print(len(img_urls),len(img_names))
        for img_url in img_urls:
            img_url="https://car.autohome.com.cn"+img_url
            yield scrapy.Request(url=img_url, callback=self.parse_url1, dont_filter=True)

    def parse_url1(self, response):
        img_urls = response.xpath('//div[@class="uibox-con carpic-list02"]/ul/li/a/@href').extract()
        for img_url in img_urls:
            img_url="https://car.autohome.com.cn"+img_url
            yield scrapy.Request(url=img_url, callback=self.parse_url2, dont_filter=True)

    def parse_url2(self, response):
        img_urls = response.xpath('//a[@class="more"]/@href').extract()
        for img_url in img_urls:
            img_url = "https://car.autohome.com.cn" + img_url
            yield scrapy.Request(url=img_url, callback=self.parse_url3, dont_filter=True)

    def parse_url3(self, response):
        img_urls = response.xpath('//div[@class="uibox-con carpic-list03 border-b-solid"]/ul/li/div/a/@href').extract()
        for img_url in img_urls:
            img_url = "https://car.autohome.com.cn" + img_url
            yield scrapy.Request(url=img_url, callback=self.parse_url4, dont_filter=True)

        next_urls = response.xpath('//a[@class="page-item-next"]/@href').extract()
        for next_url in next_urls:
            next_url = "https://car.autohome.com.cn" + next_url
            yield scrapy.Request(url=next_url, callback=self.parse_url3, dont_filter=True)

    def parse_url4(self, response):
        img_urls = response.xpath('//img[@id="img"]/@src').extract()
        img_name1 = response.xpath('//a[@class="pic-info-tit"]/text()').extract()
        img_name2 = response.xpath('//a[@class="red"]/text()').extract()
        # print(type(img_urls),img_urls[0],type(img_names),img_names[0])
        img_url = "https:"+img_urls[0]
        img_name = img_name1[0].replace(" ","")+img_name2[0].replace(" ","")
        item = ImgsItem()
        item["image_urls"] = [img_url]
        item["category"] = img_name
        yield item
