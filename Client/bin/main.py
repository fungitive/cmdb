#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-25 13:55
# @Author  : 汪菲宇
# @Site    : www.feiutech.com
# @File    : main.py
# @Software: PyCharm
#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
根据客户端信息收集脚本做成windows和linux版本。
"""
import os
import sys

BASE_DIR = os.path.dirname(os.getcwd())
# 设置工作目录，使得包和模块能够正常导入
sys.path.append(BASE_DIR)

from core import handler

if __name__ == '__main__':

    handler.ArgvHandler(sys.argv)