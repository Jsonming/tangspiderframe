# -*- coding: utf-8 -*-
import scrapy
import urllib
from tangspiderframe.items import TangspiderframeItem
from tangspiderframe.common.db import SSDBCon


class TextGermanWikiipaContentSpider(scrapy.Spider):
    name = 'text_german_wikiipa_content'
    allowed_domains = ['de.wiktionary.org']
    start_urls = ['https://de.wiktionary.org/']
    custom_settings = {
        "DOWNLOAD_DELAY": 0.3
    }

    def start_requests(self):
        ssdb_con = SSDBCon().connection()
        for i in range(220000):
            keyword = ssdb_con.lpop("dewiki_ipa_urls").decode("utf8")
            url = "https://de.wiktionary.org/w/index.php?search={}&title=Spezial%3ASuche&go=Seite&wprov=acrw1_0".format(
                urllib.parse.quote(keyword))
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={"keyword": keyword})
        ssdb_con.close()

    def parse(self, response):
        ipa_content = response.xpath("""//*[@id="mw-content-text"]/div/dl[2]/dd[1]/span/text()""").extract()
        keyword = response.meta.get("keyword")
        show_word = urllib.parse.unquote(response.url).split("/")[-1]
        item = TangspiderframeItem()
        if ipa_content:
            item['url'] = response.url
            item['title'] = keyword
            item["category"] = show_word
            item['content'] = ipa_content[0]
            yield item
