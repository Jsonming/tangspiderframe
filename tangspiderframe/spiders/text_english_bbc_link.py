# -*- coding: utf-8 -*-
import scrapy
import json
from tangspiderframe.items import TangspiderframeItem


class TextEnglishBbcLinkSpider(scrapy.Spider):
    name = 'text_english_bbc_link'
    allowed_domains = ['www.bbc.com/news/business']
    start_urls = [
        # "https://www.bbc.com/news/business-38507481",
        "https://www.bbc.com/news/business/companies",
        # "https://www.bbc.com/news/business-22434141",
        # "https://www.bbc.com/news/business-11428889",
        # "https://www.bbc.com/news/business/business_of_sport",
        # "https://www.bbc.com/news/business/economy",
        # "https://www.bbc.com/news/business/global_car_industry",
    ]

    def parse(self, response):
        links = response.xpath('//div[@class="lx-stream__feed"]//a/@href').extract()
        urls = ["https://www.bbc.com" + link for link in links if "http" not in link and "business" in link]
        urls = list(set(urls))

        frist_url = "https://push.api.bbci.co.uk/p?t=morph%3A%2F%2Fdata%2Fbbc-morph-lx-commentary-latest-data%2FassetUri%2Fnews%252Flive%252Fbusiness-47739214%2Flimit%2F31%2Fversion%2F4.1.27&c=1"
        second_url = "https://push.api.bbci.co.uk/p?t=morph%3A%2F%2Fdata%2Fbbc-morph-lx-commentary-data%2FassetUri%2Fnews%252Flive%252Fbusiness-47739214%2Flimit%2F31%2Fversion%2F5.0.24%2FwithPayload%2F11&c=1"
        three_url = "https://push.api.bbci.co.uk/p?t=morph%3A%2F%2Fdata%2Fbbc-morph-feature-toggle-manager%2FassetUri%2Fnews%252Flive%252Fbusiness-47739214%2FfeatureToggle%2Fdot-com-ads-enabled%2Fproject%2Fbbc-live%2Fversion%2F1.0.3&c=1&t=morph%3A%2F%2Fdata%2Fbbc-morph-feature-toggle-manager%2FassetUri%2Fnews%252Flive%252Fbusiness-47739214%2FfeatureToggle%2Flx-old-stream-map-rerender%2Fproject%2Fbbc-live%2Fversion%2F1.0.3&c=1&t=morph%3A%2F%2Fdata%2Fbbc-morph-feature-toggle-manager%2FassetUri%2Fnews%252Flive%252Fbusiness-47739214%2FfeatureToggle%2Freactions-stream-v4%2Fproject%2Fbbc-live%2Fversion%2F1.0.3&c=1&t=morph%3A%2F%2Fdata%2Fbbc-morph-lx-commentary-latest-data%2FassetUri%2Fnews%252Flive%252Fbusiness-47739214%2Flimit%2F21%2Fversion%2F4.1.27&c=1&t=morph%3A%2F%2Fdata%2Fbbc-morph-lx-commentary-latest-data%2FassetUri%2Fnews%252Flive%252Fbusiness-47739214%2Flimit%2F31%2Fversion%2F4.1.27&c=1"
        # yield scrapy.Request(url=frist_url, callback=self.parse_item, dont_filter=True)
        # yield scrapy.Request(url=second_url, callback=self.parse_item, dont_filter=True)
        yield scrapy.Request(url=three_url, callback=self.parse_item, dont_filter=True, meta={"page": 91})

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
                        item["url"] = "https://www.bbc.com/news/business-" + key
                        yield item

        page = response.meta.get("page")
        if page:
            if page < 101:
                new_page = page + 10
                frist_url = "https://push.api.bbci.co.uk/p?t=morph%3A%2F%2Fdata%2Fbbc-morph-lx-commentary-latest-data%2FassetUri%2Fnews%252Flive%252Fbusiness-47739214%2Flimit%2F{new_page}%2Fversion%2F4.1.27&c=1".format(
                    new_page=new_page)
                second_url = "https://push.api.bbci.co.uk/p?t=morph%3A%2F%2Fdata%2Fbbc-morph-lx-commentary-data%2FassetUri%2Fnews%252Flive%252Fbusiness-47739214%2Flimit%2F{new_page}%2Fversion%2F5.0.24%2FwithPayload%2F11&c=1".format(
                    new_page=new_page)
                three_url = "https://push.api.bbci.co.uk/p?t=morph%3A%2F%2Fdata%2Fbbc-morph-feature-toggle-manager%2FassetUri%2Fnews%252Flive%252Fbusiness-47739214%2FfeatureToggle%2Fdot-com-ads-enabled%2Fproject%2Fbbc-live%2Fversion%2F1.0.3&c=1&t=morph%3A%2F%2Fdata%2Fbbc-morph-feature-toggle-manager%2FassetUri%2Fnews%252Flive%252Fbusiness-47739214%2FfeatureToggle%2Flx-old-stream-map-rerender%2Fproject%2Fbbc-live%2Fversion%2F1.0.3&c=1&t=morph%3A%2F%2Fdata%2Fbbc-morph-feature-toggle-manager%2FassetUri%2Fnews%252Flive%252Fbusiness-47739214%2FfeatureToggle%2Freactions-stream-v4%2Fproject%2Fbbc-live%2Fversion%2F1.0.3&c=1&t=morph%3A%2F%2Fdata%2Fbbc-morph-lx-commentary-latest-data%2FassetUri%2Fnews%252Flive%252Fbusiness-47739214%2Flimit%2F{start_new_page}%2Fversion%2F4.1.27&c=1&t=morph%3A%2F%2Fdata%2Fbbc-morph-lx-commentary-latest-data%2FassetUri%2Fnews%252Flive%252Fbusiness-47739214%2Flimit%2F{new_page}%2Fversion%2F4.1.27&c=1".format(
                    start_new_page=new_page - 10, new_page=new_page)
                yield scrapy.Request(url=frist_url, callback=self.parse_item, dont_filter=True)
                yield scrapy.Request(url=second_url, callback=self.parse_item, dont_filter=True)
                yield scrapy.Request(url=three_url, callback=self.parse_item, dont_filter=True, meta={"page": new_page})
