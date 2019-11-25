#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/25 18:40
# @Author  : yangmingming
# @Site    : 
# @File    : video_download.py
# @Software: PyCharm


def you_get_download(url=None, path=None, rename=False):
    """
        调用you-get 抓取视频
    :param url: 视频url
    :param path: 存储路径
    :return:
    """
    if "win" not in sys.platform:
        path = '/data/video'
    else:
        path = './files/video'
    if not os.path.exists(path):
        os.makedirs(path)

    assert isinstance(rename, bool)  # 由于python 语言的特性，无法限制参数的类型，如果要限制类型需在代码中判断

    if rename:
        name = md5(url)
        sys.argv = ['you_get', '-o', path, '-O', name, url]
    else:
        sys.argv = ['you_get', '-o', path, url]
    you_get.main()
