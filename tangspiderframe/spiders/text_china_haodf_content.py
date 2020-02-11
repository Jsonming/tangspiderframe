# -*- coding: utf-8 -*-
import scrapy


class TextChinaHaodfContentSpider(scrapy.Spider):
    name = 'text_china_haodf_content'
    allowed_domains = ['www.haodf.com']
    start_urls = ['https://www.haodf.com/doctorteam/flow_team_6474792462.htm']

    def parse(self, response):

        dialogue = []
        case_list = response.xpath('//div[@class="f-card clearfix js-f-card"]')
        if case_list:

            # 病情描述
            illness_description = case_list[0].xpath('./div//div[@class="f-c-r-wrap"]/p[2]/text()')
            illness_description_text = illness_description[0].strip()
            dialogue.append("patient" + "\t" + illness_description_text)
