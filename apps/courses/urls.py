#！/user/bin/python
# -*- coding:utf-8 -*-
# @Time: 2018/8/7 15:04
# @Author: Envse
# @File: urls.py

from django.urls import path, include, re_path
from .views import CourseListView, CourseDetailView

app_name = "courses"

urlpatterns = [
    path('list/', CourseListView.as_view(), name='course_list'),

    # 课程机构首页url
    re_path('detail/(?P<course_id>.*)/', CourseDetailView.as_view(), name="course_detail"),

]