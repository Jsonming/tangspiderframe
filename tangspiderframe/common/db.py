#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/14 18:50
# @Author  : yangmingming
# @Site    : 
# @File    : db.py
# @Software: PyCharm
import pyssdb
from tangspiderframe import settings


class SSDBCon(object):
    def __init__(self):
        """
        初始化连接SSDB数据库
        """
        db_host = settings.SSDB_HOST
        db_port = settings.SSDB_PORT
        self.conn = pyssdb.Client(host=db_host, port=db_port)

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
            self.conn.qpush_front(name, value)
        elif isinstance(value, list) or isinstance(value, tuple):
            self.conn.qpush_front(name, " ".join(value))
        else:
            raise TypeError("insert value must be 'str', 'list' or  't")

    def close(self):
        """
        关闭数据库连接
        :return:
        """
        self.conn.close()


if __name__ == '__main__':
    conn = SSDBCon()
    conn.insert_to_list("yang", ["yang", 'ming', 'ming'])
