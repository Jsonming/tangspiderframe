# -*- coding: utf-8 -*-

import os
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys

from scrapy.pipelines.images import ImagesPipeline
from tangspiderframe.common.db import SSDBCon
from tangspiderframe import settings


class TangspiderframePipeline(object):

    def process_item(self, item, spider):
        return item


class SSDBPipeline(object):
    def __init__(self):
        self.ssdb_conn = None

    def open_spider(self, spider):
        self.ssdb_conn = SSDBCon()

    def close_spider(self, spider):
        # TODO 此处添加爬虫结束报警
        self.ssdb_conn.close()

    def process_item(self, item, spider):
        return item


class MySQLPipeline(object):

    def process_item(self, item, spider):
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
