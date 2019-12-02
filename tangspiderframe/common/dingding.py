#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/20 18:09
# @Author  : yangmingming
# @Site    : 
# @File    : dingding.py
# @Software: PyCharm
import requests
from functools import wraps
from tangspiderframe.settings import phone


def dingding_monitor(func):
    @wraps(func)
    def send_message(*args):
        url = "https://oapi.dingtalk.com/robot/send?access_token=21be857aa6e4480caaf0dda29623a9e29ad55b47d3bee9531e8f8705da56b3ee"
        headers = {'content-type': 'application/json'}
        try:
            resp = func(*args)
        except Exception as e:
            json_content = {'msgtype': "text",
                            "text": {"content": "{file_name} 异常报警,报警信息：{msg}".format(file_name=func.__name__,
                                                                                     msg=e.__str__())},
                            "at": {
                                "atMobiles": [
                                    phone
                                ],
                                "isAtAll": False
                            }}
            raise e

        else:
            json_content = {'msgtype': "text",
                            "text": {"content": "{file_name} 运行完成".format(file_name=func.__name__)},
                            "at": {
                                "atMobiles": [
                                    phone
                                ],
                                "isAtAll": False
                            }
                            }
        finally:
            flag_resp = requests.post(url=url, headers=headers, json=json_content)
            print(flag_resp.text)
        return resp

    return send_message


class DingDing(object):
    def __init__(self):
        pass

    def send(self, spider_name, result_class):
        url = "https://oapi.dingtalk.com/robot/send?access_token=21be857aa6e4480caaf0dda29623a9e29ad55b47d3bee9531e8f8705da56b3ee"
        headers = {'content-type': 'application/json'}
        json_content = {'msgtype': "text",
                        "text": {"content": "{} 测试运行{}".format(spider_name, result_class)},
                        "at": {"atMobiles": [phone],
                               "isAtAll": False}
                        }
        requests.post(url=url, headers=headers, json=json_content)


# if __name__ == '__main__':
#     dd = DingDing()
#     dd.send("爬虫", "完成")
