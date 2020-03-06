# -*- coding: utf-8 -*-
import json
import re

import emoji
import scrapy

from tangspiderframe.common.db import SSDBCon
from tangspiderframe.items import TangspiderframeItem


class TextChinaDxyContentSpider(scrapy.Spider):
    name = 'text_china_dxy_content'
    allowed_domains = ['ask.dxy.com']
    start_urls = [
        # 'https://ask.dxy.com/question/3199446',
        # 'https://ask.dxy.com/question/41487822',
        # 'https://ask.dxy.com/question/2540039',
        #
        #
        # 'https://ask.dxy.com/question/2064694',
        # 'https://ask.dxy.com/question/46831339',
        # 'https://ask.dxy.com/question/41494900',
        #
        #
        # 'https://ask.dxy.com/question/45299667',
        # 'https://ask.dxy.com/question/6100783',
        # 'https://ask.dxy.com/question/2756049',
        #
        #
        # 'https://ask.dxy.com/question/3591420',
        # 'https://ask.dxy.com/question/206912',
        # 'https://ask.dxy.com/question/41859254',
        #
        # 'https://ask.dxy.com/question/45298992',
        # 'https://ask.dxy.com/question/2433041',
        # 'https://ask.dxy.com/question/30627620'

        # 'https://ask.dxy.com/question/48035485',
        # 'https://ask.dxy.com/question/2268779',
        # 'https://ask.dxy.com/question/40460294'

        'https://ask.dxy.com/question/1916011'

    ]

    # redis_key = "text_china_dxy_link"
    # custom_settings = {
    #     'REDIS_HOST': '123.56.11.156',
    #     'REDIS_PORT': 8888,
    #     "DOWNLOAD_DELAY": 4,
    #     'REDIS_PARAMS': {
    #         'password': '',
    #         'db': 0
    #     },
    # }

    def get_link(self):
        links = []
        ssdb_con = SSDBCon().connection()
        for i in range(60):
            links.append(ssdb_con.lpop("text_china_dxy_link"))
        return links

    def delete_emoji(self, string: str):
        """
        删除颜文字
        :param string:
        :return:
        """
        sub_string = emoji.demojize(string, delimiters=("___", "___"))
        return re.sub("___(.*?)___", '', sub_string)

    def start_requests(self):
        links = self.get_link()
        for link in links:
            link = link.decode('utf8')
            print(link)
            yield scrapy.Request(url=link, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # 结构化内容
        content = response.xpath("//script/text()").extract()
        data_s = content[1].replace("window.$$data=", "")
        data = json.loads(data_s)

        # 抓取对话
        questionDialog = data.get("questionDialog")

        def parse_dialog(dialog_data):
            # 对话解析
            dialogs = []
            for dialog in dialog_data:
                dialog_type = dialog.get("type")
                dialog_content = dialog.get("content")
                dialog_content = re.sub("<.*?>|\n|\t|\r", "", dialog_content)
                if dialog_type:
                    new_content = "doctor:" + dialog_content
                else:
                    new_content = "patient:" + dialog_content
                dialogs.append(new_content)
            return "\t".join(dialogs)

        dialog = parse_dialog(questionDialog)
        dialog = self.delete_emoji(dialog)

        # 疾病类型
        disease = data.get("disease", {}).get("title")
        item = TangspiderframeItem()
        item['url'] = response.url
        item['category'] = disease
        item['content'] = dialog
        yield item
