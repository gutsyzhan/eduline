#！/user/bin/python
# -*- coding:utf-8 -*-
# @Time: 2018/8/4 16:21
# @Author: Envse
# @File: urls.py


from django.urls import path, include, re_path
from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView


app_name = "organization"

urlpatterns = [
    # 课程机构列表页url
    path("list/", OrgView.as_view(), name="org_list"),
    # 用户咨询配置url
    path("add_ask/", AddUserAskView.as_view(), name="add_ask"),
    # 课程机构首页url
    re_path('home/(?P<org_id>.*)/', OrgHomeView.as_view(), name="org_home"),
    # 机构课程列表页url
    re_path('course/(?P<org_id>.*)/', OrgCourseView.as_view(), name="org_course"),
    # 机构课程详情页url
    re_path('desc/(?P<org_id>.*)/', OrgDescView.as_view(), name="org_desc"),
    # 机构讲师详情页url
    re_path('teacher/(?P<org_id>.*)/', OrgTeacherView.as_view(), name="org_teacher"),

    # 用户收藏与取消收藏url
    path("add_fav/", AddFavView.as_view(), name="add_fav"),
]