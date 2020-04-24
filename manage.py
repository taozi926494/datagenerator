#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : manage.py
# @Time    : 2020-4-24 14:47
# @Software: PyCharm
# @Author  : Taoz
# @contact : xie-hong-tao@qq.com
# 创建数据库
from datagenerator.models.community import *

db.init_app(app)
db.create_all()
