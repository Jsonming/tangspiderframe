# -*- coding: utf-8 -*-
import scrapy


class ImgPlatesmaniaCarSpider(scrapy.Spider):
    name = 'img_platesmania_car'
    allowed_domains = ['platesmania.com/cn/gallery']
    start_urls = ['http://platesmania.com']

    def parse(self, response):
        print(response.text)
