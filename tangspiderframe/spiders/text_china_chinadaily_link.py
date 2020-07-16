# -*- coding: utf-8 -*-
import re
import scrapy
from tangspiderframe.items import TangspiderframeItem


class TextChinaChinadailyLinkSpider(scrapy.Spider):
    name = 'text_china_chinadaily_link'
    allowed_domains = ['cn.chinadaily.com.cn']
    start_urls = [
        # 时政
        'https://china.chinadaily.com.cn/5bd5639ca3101a87ca8ff636',

        "https://china.chinadaily.com.cn/5bd5639ca3101a87ca8ff634",
        "https://china.chinadaily.com.cn/5bd5639ca3101a87ca8ff634/5bd5669ba3101a87ca8ff66a",
        "https://cn.chinadaily.com.cn/5b753f9fa310030f813cf408/5b940cbaa310030f813ed4d7",
        "https://china.chinadaily.com.cn/5bd5639ca3101a87ca8ff634/5bd5669ba3101a87ca8ff660",
        "https://china.chinadaily.com.cn/5bd5639ca3101a87ca8ff634/5bd5669ba3101a87ca8ff666",
        "https://china.chinadaily.com.cn/5bd5639ca3101a87ca8ff634/5bd5669ba3101a87ca8ff662",

        'https://china.chinadaily.com.cn/hexin/5bd5656fa3101a87ca8ff64a',
        "https://china.chinadaily.com.cn/hexin/5bd5656fa3101a87ca8ff64e",
        "https://china.chinadaily.com.cn/hexin/5bd5656fa3101a87ca8ff650",

        "https://china.chinadaily.com.cn/theory",
        "https://china.chinadaily.com.cn/theory/5bd56628a3101a87ca8ff656",
        "https://china.chinadaily.com.cn/theory/5bd56628a3101a87ca8ff65a",
        "https://china.chinadaily.com.cn/theory/5bd56628a3101a87ca8ff65c",
        "https://china.chinadaily.com.cn/theory/5bd56628a3101a87ca8ff65e",
        "https://china.chinadaily.com.cn/theory/5bd56628a3101a87ca8ff654",

        "https://tw.chinadaily.com.cn/5e1ea9f6a3107bb6b579a144",
        "https://tw.chinadaily.com.cn/5e1ea9f6a3107bb6b579a147",
        "https://tw.chinadaily.com.cn/5e1ea9f6a3107bb6b579a14a",
        "https://tw.chinadaily.com.cn/5e23b3dea3107bb6b579ab65",

        # 资讯
        "https://world.chinadaily.com.cn/5bd55927a3101a87ca8ff618",
        "https://world.chinadaily.com.cn/5bd55927a3101a87ca8ff614",
        "https://world.chinadaily.com.cn/5bd55927a3101a87ca8ff610",
        "https://world.chinadaily.com.cn/5bda6641a3101a87ca904fe6",
        "https://world.chinadaily.com.cn/5bd97038a3101a87ca904233/5bfb8e6aa3101a87ca945954",
        "https://world.chinadaily.com.cn/5bd55927a3101a87ca8ff616/5bd559a9a3101a87ca8ff61c",
        "https://world.chinadaily.com.cn/5bd55927a3101a87ca8ff616/5bd559a9a3101a87ca8ff61e",
        "https://world.chinadaily.com.cn/5bd55927a3101a87ca8ff616/5bd559a9a3101a87ca8ff620",
        "https://world.chinadaily.com.cn/5bd55927a3101a87ca8ff616/5bd559a9a3101a87ca8ff624",

        "https://world.chinadaily.com.cn/5bd55927a3101a87ca8ff618",
        "https://cnews.chinadaily.com.cn/5bd5693aa3101a87ca8ff676",
        "https://cnews.chinadaily.com.cn/5bd5693aa3101a87ca8ff67a",
        "https://china.chinadaily.com.cn/5bd8126ba3101a87ca90094b/5bfe4ee1a3101a87ca9463de",
        "https://cnews.chinadaily.com.cn/5bd90f5da3101a87ca90263b/2018tpgj",
        "https://cnews.chinadaily.com.cn/5bd5696ea3101a87ca8ff684",
        "https://cnews.chinadaily.com.cn/5bd90f5da3101a87ca90263b",
        "https://cnews.chinadaily.com.cn/5bd5696ea3101a87ca8ff680",
        "https://cn.chinadaily.com.cn/5b753f9fa310030f813cf408/5b9408aca310030f813ed4d4",
        "https://cn.chinadaily.com.cn/5b753f9fa310030f813cf408/5bd54dd6a3101a87ca8ff5f8/5bd54e59a3101a87ca8ff606",
        "https://cn.chinadaily.com.cn/5b753f9fa310030f813cf408/5b9408aca310030f813ed4d4/5bd54828a3101a87ca8ff5c6",

        "https://caijing.chinadaily.com.cn/5b7620c4a310030f813cf452",
        "https://finance.chinadaily.com.cn/5b761eb1a310030f813cf43a",
        "https://finance.chinadaily.com.cn/5b761eb1a310030f813cf43a",
        "https://finance.chinadaily.com.cn/5b761ed0a310030f813cf43c",
        "https://finance.chinadaily.com.cn/5b761ea4a310030f813cf439",
        "https://finance.chinadaily.com.cn/5b9799c1a310f8f8a09b240b",
        "https://finance.chinadaily.com.cn/5b761e81a310030f813cf438",
        "https://finance.chinadaily.com.cn/5b761ef4a310030f813cf43e",
        "https://finance.chinadaily.com.cn/5b8f7837a310030f813ed4cc",
        "https://che.chinadaily.com.cn/5b7626cda310030f813cf477",
        "https://che.chinadaily.com.cn/5b7626cda310030f813cf46c",
        "https://che.chinadaily.com.cn/5b7626cda310030f813cf476",
        "https://che.chinadaily.com.cn/5b7626cda310030f813cf473",
        "https://che.chinadaily.com.cn/5b7626cda310030f813cf475",
        "https://che.chinadaily.com.cn/5b7626cda310030f813cf472",
        "https://che.chinadaily.com.cn/5b7626cda310030f813cf474",
        "https://che.chinadaily.com.cn/5b7626cda310030f813cf470",
        "https://che.chinadaily.com.cn/5b8f780ea310030f813ed4ca",
        "https://tech.chinadaily.com.cn/5b7621d3a310030f813cf45b",
        "https://tech.chinadaily.com.cn/5b762218a310030f813cf45f",
        "https://tech.chinadaily.com.cn/5b762186a310030f813cf457",
        "https://tech.chinadaily.com.cn/5b76219ca310030f813cf458",
        "https://tech.chinadaily.com.cn/5b7621aaa310030f813cf459",
        "https://tech.chinadaily.com.cn/5b8f760ea310030f813ed4c4",
        "https://qiye.chinadaily.com.cn/5b7627bba310030f813cf480",
        "https://qiye.chinadaily.com.cn/5b7627bba310030f813cf481",
        "https://qiye.chinadaily.com.cn/5b7627bba310030f813cf484",
        "https://qiye.chinadaily.com.cn/5b7627bba310030f813cf486",
        "https://qiye.chinadaily.com.cn/5bac42f8a3101a87ca8feb34",
        "https://ent.chinadaily.com.cn/5b761f98a310030f813cf43f",
        "https://fang.chinadaily.com.cn/5b75426aa310030f813cf41c",
        "https://fang.chinadaily.com.cn/5b75426aa310030f813cf418",
        "https://fang.chinadaily.com.cn/5b75426aa310030f813cf416",
        "https://fang.chinadaily.com.cn/5b75426aa310030f813cf419",
        "https://fang.chinadaily.com.cn/5b75426aa310030f813cf41b",
        "https://fang.chinadaily.com.cn/5b75426aa310030f813cf41d",
        "https://caijing.chinadaily.com.cn/finance/",
        "https://ent.chinadaily.com.cn/5b761f98a310030f813cf43f",
        "https://ent.chinadaily.com.cn/5b761f98a310030f813cf440",
        "https://ent.chinadaily.com.cn/5b761f98a310030f813cf445",
        "https://ent.chinadaily.com.cn/5b761f98a310030f813cf442",
        "https://ent.chinadaily.com.cn/5b761f98a310030f813cf446",
        "https://ent.chinadaily.com.cn/5b761f98a310030f813cf447",
        "https://ent.chinadaily.com.cn/5b761f98a310030f813cf441",
        "https://ent.chinadaily.com.cn/5b761f98a310030f813cf443",
        "https://ent.chinadaily.com.cn/5b761f98a310030f813cf444",
        "https://ent.chinadaily.com.cn/5b761f98a310030f813cf448",
        "https://ent.chinadaily.com.cn/5b8f7721a310030f813ed4c6",
        "https://cn.chinadaily.com.cn/lvyou/5b7628dfa310030f813cf495",
        "https://cn.chinadaily.com.cn/lvyou/5b7628c6a310030f813cf48a",
        "https://cn.chinadaily.com.cn/lvyou/5b7628c6a310030f813cf48c",
        "https://cn.chinadaily.com.cn/lvyou/5b7628c6a310030f813cf48b",
        "https://cn.chinadaily.com.cn/lvyou/5b7628c6a310030f813cf492",
        "https://cn.chinadaily.com.cn/lvyou/5b7628c6a310030f813cf493",
        "https://cn.chinadaily.com.cn/lvyou/5bac7d20a3101a87ca8ff52d",
        "https://fashion.chinadaily.com.cn/5b762404a310030f813cf467",
        "https://cn.chinadaily.com.cn/jiankang",
        "https://fashion.chinadaily.com.cn/5b762404a310030f813cf461",
        "https://fashion.chinadaily.com.cn/5b762404a310030f813cf462",
        "https://fashion.chinadaily.com.cn/5b762404a310030f813cf463",
        "https://fashion.chinadaily.com.cn/5b8f77a7a310030f813ed4c8",

    ]

    def parse(self, response):
        links = response.xpath('//div[contains(@class, "busBox")]//h3/a/@href').extract()
        for link in links:
            item = TangspiderframeItem()
            item['url'] = "https:" + link
            yield item

        next_page = response.xpath('//*[@id="div_currpage"]//a[contains(text(), "下一页")]/@href').extract()
        if next_page:
            next_page_url = "https:" + next_page[0]
            yield scrapy.Request(url=next_page_url, dont_filter=True, callback=self.parse)
