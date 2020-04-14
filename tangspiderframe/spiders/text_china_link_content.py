# -*- coding: utf-8 -*-
import scrapy
import re
from tangspiderframe.items import TangspiderframeItem


class TextChinaLinkContentSpider(scrapy.Spider):
    name = 'text_china_link_content'
    allowed_domains = ['ecp.sgcc.com.cn']
    start_urls = [
        'http://ecp.sgcc.com.cn/news_list.jsp?site=global&column_code=014001007&company_id=00&news_name=all&pageNo={}'.format(i) for i in range(1, 326)]

    def parse(self, response):
        info_li = response.xpath('//ul[@class="newslist01"]/li')
        for item in info_li:
            item_time = item.xpath("./span/text()").extract()
            if item_time:
                item_time = item_time[0].strip()
            else:
                item_time = ''

            item_name = item.xpath("./a/@title").extract()
            if item_name:
                item_name = item_name[0].replace("\r", '').replace("\t", '').replace("\n", '')
            else:
                item_name = ""

            item_detail_id = item.xpath("./a/@onclick").extract()
            if item_detail_id:
                detail_id = item_detail_id[0].replace("showNewsDetail(", '').replace(");", '')
                item_id = [i.replace("'", '').replace('"', "").strip() for i in detail_id.split(",")]
            else:
                item_id = ()

            item_company = item.xpath("./a/text()").extract()
            if item_company:
                company_name = re.findall("\[.*?\]", item_company[0])
                item_company_name = company_name[0].replace("[", '').replace(']', "")
            else:
                item_company_name = ""
            url = r"http://ecp.sgcc.com.cn/html/news/{}/{}.html".format(*item_id)

            item = TangspiderframeItem()
            item['url'] = url  # 详情页链接
            item['category'] = item_company_name  # 类别存储招标公司
            item['content'] = item_name  # 招标时间
            item['title'] = item_time
            yield item
