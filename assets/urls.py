#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-25 14:05
# @Author  : 汪菲宇
# @Site    : www.feiutech.com
# @File    : urls.py
# @Software: PyCharm

from django.urls import path
from assets import views

app_name = 'assets'

urlpatterns = [
    path('report/', views.report, name='report'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('index/', views.index, name='index'),
    path('detail/<int:asset_id>/', views.detail, name="detail"),
    path('', views.dashboard),
]