# -*- coding: utf-8 -*-
import re
import scrapy
from tangspiderframe.items import TangspiderframeItem
from tangspiderframe.common.db import SSDBCon


class TextKoreaDongaContentSpider(scrapy.Spider):
    name = 'text_korea_donga_content'
    allowed_domains = ['kids.donga.com']
    start_urls = [
        r"https://kids.donga.com/?ptype=article&no=20201006130853145240&psub=world&gbn=01",
        'https://kids.donga.com/?ptype=article&no=20201006130646769983&psub=world&gbn=01'
    ]

    def start_requests(self):
        ssdb_con = SSDBCon().connection()
        for i in range(1000):
            item = ssdb_con.rpop("text_korea_donga_link")
            url = item.decode("utf8").replace("https://kids.donga.com", "https://kids.donga.com/")
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        content = []
        at_content = response.xpath("//div[@class='content']//div[@class='at_content']/text()").extract()
        content.extend(at_content)
        other_content = response.xpath(
            "//div[@class='content']//div[@class='at_content']//*[not(self::script)]/text()").extract()
        content.extend(other_content)
        new_content = ""
        for para in content:
            para_content = para.strip()
            ending_flag = re.findall(r"[▶].*?@donga\.com", para_content, re.S)
            if ending_flag:
                break
            else:
                new_content += para_content + "\n"
        item = TangspiderframeItem()
        item['url'] = response.url
        item['content'] = new_content
        return item
