# -*- coding: utf-8 -*-
import re
import json
import requests
import scrapy
from lxml import etree
from tangspiderframe.items import TangspiderframeItem
from scrapy_redis.spiders import RedisSpider


class TextChinaHaodfContentSpider(RedisSpider):
    name = 'text_china_haodf_content'
    allowed_domains = ['www.haodf.com']
    start_urls = ['https://www.haodf.com/doctorteam/flow_team_6474527962.htm']

    redis_key = "text_china_haodf_link"
    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def __init__(self):
        self.headers = {
            'cache-control': "no-cache",
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        self.resp = None
        self.url = None

    def crawl_get(self, url, headers=None):
        # 抓取翻页
        if headers:
            _headers = headers
        else:
            _headers = self.headers

        response = requests.request("GET", url, headers=_headers)
        self.resp = response.text

    def parse_html(self, resp):
        # 其他页对话内容
        data = []
        root = etree.HTML(resp)
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
        return data

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
                for i in range(2, int(s_p) + 1):
                    new_url = response.url.replace(".htm", '_{}.htm'.format(i))
                    self.crawl_get(new_url)
                    dialogue.extend(self.parse_html(self.resp))

        item = TangspiderframeItem()
        item['url'] = response.url
        item['category'] = illness_text
        item['content'] = "\t".join(dialogue)
        yield item
