# -*- coding: utf-8 -*-

import os
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys

from scrapy.pipelines.images import ImagesPipeline
from tangspiderframe.common.db import SSDBCon, MysqlCon
from tangspiderframe import settings
from tangspiderframe.common.dingding import DingDing


class TangspiderframePipeline(object):

    def process_item(self, item, spider):
        return item


class SSDBPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        self.ssdb_conn = SSDBCon()

    def close_spider(self, spider):
        dd = DingDing()
        dd.send(spider.name, "")
        self.ssdb_conn.close()

    def process_item(self, item, spider):
        if spider.name.endswith("link"):
            if not self.ssdb_conn.exist_finger(spider.name, item["url"]):
                self.ssdb_conn.insert_to_list(spider.name, item["url"])
                self.ssdb_conn.insert_finger(spider.name, item["url"])
                return item
        elif spider.name.endswith("content"):
            if not self.ssdb_conn.exist_finger(spider.name, item["url"]):
                self.ssdb_conn.insert_finger(spider.name, item["url"])
                return item


class MySQLPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        self.conn = MysqlCon()

        # 文本类型爬虫，抓取类型为内容（content字段）自动创建表
        if spider.name.startswith("text") and spider.name.endswith("content"):
            if not self.conn.exist_table(spider.name):
                self.conn.create_table(spider.name)

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        if item:
            if not item.get("images") and not spider.name.endswith("link"):
                self.conn.insert_data(spider.name, item)
            return item


class ImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # 这个方法是在发送下载请求之前调用的，其实这个方法本身就是去发送下载请求的
        request_objs = super(ImagePipeline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        # 这个方法是在图片将要被存储的时候调用，来获取这个图片存储的路径
        path = super(ImagePipeline, self).file_path(request, response, info)
        category = request.item.get('category')
        image_store = settings.IMAGES_STORE
        category_path = os.path.join(image_store, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)

        # windows 平台和liunx平台分开
        if "win" in sys.platform:
            image_name = path.replace("full/", '')
            image_path = os.path.join(category_path, image_name)
        else:
            image_path = path.replace("full/", category + "/")
        return image_path
