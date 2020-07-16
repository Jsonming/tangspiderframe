#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/20 19:55
# @Author  : yangmingming
# @Site    : ww
# @File    : main.py
# @Software: PyCharm

from scrapy import cmdline

cmdline.execute("scrapy crawl text_china_chinadaily_link".split())
