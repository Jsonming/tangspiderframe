# -*- coding: utf-8 -*-
import copy
import re

import scrapy
from lxml import etree
from scrapy_redis.spiders import RedisSpider

from tangspiderframe.items import TangspiderframeItem


# class TextChinaHaodfContentSpider(scrapy.Spider):
class TextChinaHaodfContentSpider(RedisSpider):

    name = 'text_china_haodf_content'
    allowed_domains = ['www.haodf.com']
    start_urls = [
        # 'https://www.haodf.com/wenda/doctorhelen_g_4894216235.htm',
        # "https://www.haodf.com/wenda/drleiyu_g_4823354104.htm",
        # 'https://www.haodf.com/wenda/lq9850804_g_4827618952.htm',
        # 'https://www.haodf.com/wenda/zhengsufen_g_4832242866.htm',
        # 'https://www.haodf.com/wenda/yaoxiaoyan2009_g_4821369677.htm',
        # 'https://www.haodf.com/wenda/wanghuhufuting88_g_4836339282.htm',
        # 'https://www.haodf.com/wenda/wangkuanfeng123_g_4839870138.htm',
        # 'https://www.haodf.com/wenda/tangjuyu_g_4920732998.htm',
        # 'https://www.haodf.com/wenda/zhuzexing_g_4926528399.htm',
        # 'https://www.haodf.com/wenda/mmzz_g_4894214560.htm',
        'https://www.haodf.com/wenda/fushaomei_g_4761255296.htm'
    ]

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
        second_case = response.xpath('//div[@class="h_s_cons_info"]/div[@class="h_s_info_cons"]')

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
            # 翻页
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
        elif second_case:
            # 第二种情况
            # 疾病
            illness = second_case[0].xpath('./h2[1]//text()').extract()
            illness_text = ''.join(illness).strip().replace('\n', '').replace('\t', '').replace('\r', '')
            dialogue.append("illness" + ":" + illness_text)

            #病情描述
            illness_description = second_case[0].xpath('./div[1]/text()').extract()
            illness_description_text = ''.join(illness_description).replace('病情描述：', '').strip()
            illness_description_text = illness_description_text.replace('\t', '').replace('\n', '').replace('\r', '')
            dialogue.append("patient" + ":" + illness_description_text)

            # 对话
            steam = response.xpath('//div[@class="stream_yh_right"]/div')
            for item in steam:
                tag = item.xpath('./@class').extract()
                if tag:
                    tag = tag[0]
                    if tag == "h_s_cons_docs":
                        content = item.xpath('./h3[@class="h_s_cons_title"]/text()').extract()
                        talk = "doctor" + ":" + ''.join(content).strip().replace('\n', '').replace('\t', '').replace('\r', '')
                        dialogue.append(talk)
                    elif tag == "h_s_cons":
                        content = item.xpath('./pre/text()').extract()
                        talk = "patient" + ":" + ''.join(content).strip().replace('\n', '').replace('\t', '').replace('\r', '')
                        dialogue.append(talk)

            item = TangspiderframeItem()
            item['url'] = response.url
            item['category'] = illness_text
            item['content'] = "\t".join(dialogue)
            yield item