# -*- coding: utf-8 -*-
import scrapy
import json
from urllib.parse import quote
import time
from tangspiderframe.items import TangspiderframeItem


class TextEnglishBbcLinkSpider(scrapy.Spider):
    name = 'text_english_bbc_link'
    allowed_domains = ['www.bbc.com/news/business']
    start_urls = [
        # "https://www.bbc.com/news/business-38507481",
        # "https://www.bbc.com/news/business/companies",
        # "https://www.bbc.com/news/business-22434141",
        # "https://www.bbc.com/news/business-11428889",
        # "https://www.bbc.com/news/business/business_of_sport",
        # "https://www.bbc.com/news/business/economy",
        # "https://www.bbc.com/news/business/global_car_industry",

        # "https://www.bbc.com/news/technology"

        # "https://www.bbc.com/news/science_and_environment"
        # "https://www.bbc.com/news/stories"

        # "https://www.bbc.com/news/entertainment_and_arts"
        "https://www.bbc.com/news/health"
    ]

    def __init__(self):
        self.type_id = "47639448"
        self.t = "health"

    def parse(self, response):
        links = response.xpath('//div[@class="lx-stream__feed"]//a/@href').extract()
        links.extend(response.xpath('//div[@class="mpu-available"]//a/@href').extract())
        links.extend(response.xpath('//div[@role="region"]//a/@href').extract())

        urls = ["https://www.bbc.com" + link for link in links if "http" not in link]
        urls = list(set(urls))
        for url in urls:
            item = TangspiderframeItem()
            item["url"] = url
            yield item

        type_id = self.type_id
        t = self.t
        base_url = "https://push.api.bbci.co.uk/p?"
        one_arg = "morph://data/bbc-morph-lx-commentary-latest-data/assetUri/news%2Flive%2F{}-{}/limit/31/version/4.1.27".format(
            t, type_id)
        one_url = "t={}&c=1".format(quote(one_arg, safe=''))
        frist_url = base_url + one_url

        two_arg = "morph://data/bbc-morph-lx-commentary-data/assetUri/news%2Flive%2F{}-{}/limit/31/version/5.0.24/withPayload/11".format(
            t, type_id)
        two_url = "t={}&c=1".format(quote(two_arg, safe=''))
        second_url = base_url + two_url

        three_arg_1 = "morph://data/bbc-morph-feature-toggle-manager/assetUri/news%2Flive%2F{}-{}/featureToggle/dot-com-ads-enabled/project/bbc-live/version/1.0.3".format(
            t, type_id)
        three_arg_2 = "morph://data/bbc-morph-feature-toggle-manager/assetUri/news%2Flive%2F{}-{}/featureToggle/lx-old-stream-map-rerender/project/bbc-live/version/1.0.3".format(
            t, type_id)
        three_arg_3 = "morph://data/bbc-morph-feature-toggle-manager/assetUri/news%2Flive%2F{}-{}/featureToggle/reactions-stream-v4/project/bbc-live/version/1.0.3".format(
            t, type_id)
        three_arg_4 = "morph://data/bbc-morph-lx-commentary-latest-data/assetUri/news%2Flive%2F{}-{}/limit/21/version/4.1.27".format(
            t, type_id)
        three_arg_5 = "morph://data/bbc-morph-lx-commentary-latest-data/assetUri/news%2Flive%2F{}-{}/limit/31/version/4.1.27".format(
            t, type_id)
        arg = []
        for item in [three_arg_1, three_arg_2, three_arg_3, three_arg_4, three_arg_5]:
            arg.append(quote(item, safe=''))

        three_url = "t={}&c=1&t={}&c=1&t={}&c=1&t={}&c=1&t={}&c=1".format(*arg)
        three_url = base_url + three_url

        yield scrapy.Request(url=frist_url, callback=self.parse_item, dont_filter=True)
        yield scrapy.Request(url=second_url, callback=self.parse_item, dont_filter=True)
        yield scrapy.Request(url=three_url, callback=self.parse_item, dont_filter=True, meta={"page": 31})

    def parse_item(self, response):
        resp = json.loads(response.text)

        moments = resp.get("moments")
        if moments:
            for moment in moments:
                payload = json.loads(moment.get("payload"))
                if isinstance(payload, list):
                    for item in payload:
                        key = item.get("key")
                        item = TangspiderframeItem()
                        item["url"] = "https://www.bbc.com/news/{}-".format(self.t) + key
                        yield item

        page = response.meta.get("page")
        if page:
            if page < 211:
                new_page = page + 10
                type_id = self.type_id

                base_url = "https://push.api.bbci.co.uk/p?"
                one_arg = "morph://data/bbc-morph-lx-commentary-latest-data/assetUri/news%2Flive%2F{}-{}/limit/{}/version/4.1.27".format(
                    self.t, type_id, new_page)
                one_url = "t={}&c=1".format(quote(one_arg, safe=''))
                frist_url = base_url + one_url

                two_arg = "morph://data/bbc-morph-lx-commentary-data/assetUri/news%2Flive%2F{}-{}/limit/{}/version/5.0.24/withPayload/11".format(
                    self.t, type_id, new_page)
                two_url = "t={}&c=1".format(quote(two_arg, safe=''))
                second_url = base_url + two_url

                three_arg = "morph://data/bbc-morph-lx-commentary-latest-data/assetUri/news%2Flive%2F{}-{}/limit/{}/version/4.1.27".format(
                    self.t, type_id, new_page)

                three_url = "&t={}&c=1".format(quote(three_arg, safe=''))
                three_url = response.url + three_url

                yield scrapy.Request(url=frist_url, callback=self.parse_item, dont_filter=True)
                yield scrapy.Request(url=second_url, callback=self.parse_item, dont_filter=True)
                yield scrapy.Request(url=three_url, callback=self.parse_item, dont_filter=True, meta={"page": new_page})
