#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-25 13:58
# @Author  : 汪菲宇
# @Site    : www.feiutech.com
# @File    : settings.py
# @Software: PyCharm

import os

# 远端接收数据的服务器
Params = {
    "server": "127.0.0.1",
    "port": 8000,
    'url': '/assets/report/',
    'request_timeout': 30,
}

# 日志文件配置
PATH = os.path.join(os.path.dirname(os.getcwd()), 'log', 'cmdb.log')