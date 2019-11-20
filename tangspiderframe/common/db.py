#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/14 18:50
# @Author  : yangmingming
# @Site    : 
# @File    : db.py
# @Software: PyCharm
import redis
from tangspiderframe import settings
from tangspiderframe.common.common import md5


class SSDBCon(object):
    def __init__(self):
        """
        初始化连接SSDB数据库,
        链接SSDB数据库没有使用SSDB客户端，使用的是Redis客户端有两个原因
            1.可以无缝对接
            2.框架配合scrapy_redis使用
            3.这里的函数，没有删除数据函数，如果要执行删除操作 到数据库删除  SSDB数据库命令参考 http://ssdb.io/docs/zh_cn/commands/index.html

        """
        db_host = settings.SSDB_HOST
        db_port = settings.SSDB_PORT
        self.conn = redis.StrictRedis(host=db_host, port=db_port)

    def connection(self):
        """
        返回数据库连接
        :return:
        """
        return self.conn

    def insert_to_list(self, name, value):
        """
        向列表中插入单个的值
        :param name: 列表名称
        :param value: 要插入的值
        :return:
        """
        if isinstance(value, str):
            self.conn.lpush(name, value)
        elif isinstance(value, list) or isinstance(value, tuple):
            self.conn.lpush(name, *value)

    def get_list(self, name, start=0, end=-1):
        """
        获取列表的内容
        :param name:
        :param start: 开始索引
        :param end: 结束索引
        :return:
        """
        return self.conn.lrange(name=name, start=start, end=end)

    def insert_to_set(self, name, value):
        """
        插入到集合中,由于SSDB 没有set数据类型， 这里的集合采用排序集合sorted set
        :return:
        """
        if isinstance(value, str):
            maping = {value: 1}
        elif isinstance(value, list) or isinstance(value, tuple):
            maping = {item: 1 for item in value}

        self.conn.zadd(name, mapping=maping)

    def insert_finger(self, name, value):
        """
        将字符串md5插入集合
        :param name:
        :param value:
        :return:
        """
        self.insert_to_set(name, md5(value))

    def exist_finger(self, name, value):
        """
        判断指纹是否存在
        :param name:
        :param value:
        :return:
        """
        return self.exist_in_set(name, md5(value))

    def get_set(self, name, start=0, end=-1):
        """
        获取集合中的元素
        :param name:
        :return:
        """
        return self.conn.zrange(name=name, start=start, end=end)

    def exist_in_set(self, name, value):
        """
        判断值是否在集合中
        :param name: 集合名称
        :param value: 值
        :return:
        """
        return self.conn.zscore(name, value)

    def close(self):
        """
        关闭数据库连接
        :return:
        """
        self.conn.connection_pool.disconnect()


if __name__ == '__main__':
    conn = SSDBCon()
    # conn.insert_to_list("yang", ["yang", 'ming', 'ming'])
    # r = conn.get_list(name='text_speechocean_link')
    # print(r)

    # conn.insert_to_set("ming", ["sdhfioasd", "sdhjfklad", "sdhjfkal"])
    # r = conn.get_set("ming")
    # print(r)
    # r = conn.exist_in_set("ming", "sdhjfkad")
    r = conn.connection()
    print(r)
