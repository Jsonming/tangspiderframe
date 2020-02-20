# -*- coding: utf-8 -*-
import re
import time
import json
import requests
import copy
import scrapy
from lxml import etree
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider


class TextChinaHaodfContentSpider(RedisSpider):
    name = 'text_china_haodf_content'
    allowed_domains = ['www.haodf.com']
    start_urls = ['https://www.haodf.com/doctorteam/flow_team_6467409873.htm']

    redis_key = "text_china_haodf_link"
    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse_html(self, response):
        # 其他页对话内容
        data = []
        root = etree.HTML(response.text)
        case_list = root.xpath('//div[@class="f-card clearfix js-f-card"]')
        for case in case_list:
            content_ele = case.xpath('./div//div[@class="f-c-r-wrap"]//p')
            if content_ele:
                content_ele = content_ele[0]
                content = ''.join(content_ele.xpath('.//text()'))
                class_name = content_ele.xpath('./@class')[0]
                if class_name == "f-c-r-doctext":
                    data.append("doctor" + ":" + content.strip().replace('\n', '').replace('\t', '').replace('\r', ''))
                elif class_name == "f-c-r-w-text":
                    data.append("patient" + ":" + content.strip().replace('\n', '').replace('\t', '').replace('\r', ''))

        current_page_data = "\t".join(data)
        previous_page = copy.deepcopy(response.meta)
        content = previous_page.get("content")
        new_content = content + "\t" + current_page_data
        current_page = previous_page.get("page") + 1
        sum_page = previous_page.get("sum_page")
        if current_page < sum_page:
            new_data = previous_page
            new_data["content"] = new_content
            new_data["page"] = current_page
            new_url = re.sub("_(\d+).htm", "_{}.htm".format(current_page + 1), response.url)
            yield scrapy.Request(url=new_url, callback=self.parse_html, meta=new_data)
        else:
            item = TangspiderframeItem()
            item['url'] = previous_page.get("url")
            item['category'] = previous_page.get("category")
            item['content'] = new_content
            yield item

    def parse(self, response):
        dialogue, illness_text = [], ''

        # 第一个版本抓取
        case_list = response.xpath('//div[@class="f-card clearfix js-f-card"]')
        if case_list:
            # 疾病
            illness = case_list[0].xpath('./div//div[@class="f-c-r-wrap"]/p[1]/text()').extract()
            illness_text = illness[0].strip().replace('\n', '').replace('\t', '').replace('\r', '')
            dialogue.append("illness" + ":" + illness_text)

            # 病情描述
            illness_description = case_list[0].xpath('./div//div[@class="f-c-r-wrap"]/p[2]/text()').extract()
            illness_description_text = illness_description[0].strip().replace('\n', '').replace('\t', '').replace('\r',
                                                                                                                  '')
            dialogue.append("patient" + ":" + illness_description_text)

            # 患者医生对话
            for case in case_list[1:]:
                content_ele = case.xpath('./div//div[@class="f-c-r-wrap"]//p')
                if content_ele:
                    content_ele = content_ele[0]
                    content = ''.join(content_ele.xpath('.//text()').extract())

                    class_name = content_ele.xpath('./@class').extract()[0]
                    if class_name == "f-c-r-doctext":
                        dialogue.append(
                            "doctor" + ":" + content.strip().replace('\n', '').replace('\t', '').replace('\r', ''))
                    elif class_name == "f-c-r-w-text":
                        dialogue.append(
                            "patient" + ":" + content.strip().replace('\n', '').replace('\t', '').replace('\r', ''))

            sum_page = response.xpath('/html//a[@class="page_turn_a"][@rel="true"]//text()').extract()
            if sum_page:
                s_p = re.findall('\d+', sum_page[0])[0]
                data = {
                    "url": response.url,
                    'category': "illness_text",
                    "content": "\t".join(dialogue),
                    "page": 1,
                    "sum_page": int(s_p),
                }
                new_url = response.url.replace(".htm", '_{}.htm'.format(2))
                yield scrapy.Request(url=new_url, callback=self.parse_html, meta=data)
            else:
                item = TangspiderframeItem()
                item['url'] = response.url
                item['category'] = illness_text
                item['content'] = "\t".join(dialogue)
                yield item
