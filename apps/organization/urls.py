#！/user/bin/python
# -*- coding:utf-8 -*-
# @Time: 2018/8/4 16:21
# @Author: Envse
# @File: urls.py


from django.urls import path, include, re_path
from .views import OrgView, AddUserAskView


app_name = "organization"

urlpatterns = [
    # 课程机构列表页url
    path("list/", OrgView.as_view(), name="org_list"),
    # 用户咨询配置url
    path("add_ask/", AddUserAskView.as_view(), name="add_ask"),
]