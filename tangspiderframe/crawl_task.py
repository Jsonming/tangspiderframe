#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/10 15:33
# @Author  : yangmingming
# @Site    : 
# @File    : crawl_task.py
# @Software: PyCharm

from multiprocessing import Process
from scrapy import cmdline
import time
import logging

# 配置参数即可, 爬虫名称，
confs = [
    {
        "spider_name": "it",
        "sleep": 2,
    },
]


def start_spider(spider_name, frequency):
    args = ["scrapy", "crawl", spider_name]
    while True:
        start = time.time()
        p = Process(target=cmdline.execute, args=(args,))
        p.start()
        p.join()
        logging.debug("### use time: %s" % (time.time() - start))
        time.sleep(frequency)


if __name__ == '__main__':
    for conf in confs:
        process = Process(target=start_spider, args=(conf["spider_name"], conf["sleep"]))
        process.start()
