# -*- coding: utf-8 -*-
import json
import re

import emoji
from scrapy_redis.spiders import RedisSpider

from tangspiderframe.items import TangspiderframeItem


class TextChinaDxyContentSpider(RedisSpider):
    name = 'text_china_dxy_content'
    allowed_domains = ['ask.dxy.com']
    start_urls = ['https://ask.dxy.com/question/2661050']

    redis_key = "text_china_dxy_link"
    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def delete_emoji(self, string: str):
        """
        删除颜文字
        :param string:
        :return:
        """
        sub_string = emoji.demojize(string, delimiters=("___", "___"))
        return re.sub("___(.*?)___", '', sub_string)

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
