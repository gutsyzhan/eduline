#！/user/bin/python
# -*- coding:utf-8 -*-
# @Time: 2018/8/7 15:04
# @Author: Envse
# @File: urls.py

from django.urls import path, include, re_path
from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentView, VideoPlayView

app_name = "courses"

urlpatterns = [
    path('list/', CourseListView.as_view(), name='course_list'),

    # 课程机构首页url
    re_path('detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name="course_detail"),

    # 课程章节信息页url
    re_path('info/(?P<course_id>\d+)/', CourseInfoView.as_view(), name="course_info"),

    # 课程评论页面url
    re_path('comment/(?P<course_id>\d+)/', CourseCommentView.as_view(), name="course_comment"),

    # 用户增加课程评论页面url
    path('add_comment/', AddCommentView.as_view(), name="add_comment"),

    # 视频播放页面url
    re_path('video/(?P<video_id>\d+)/', VideoPlayView.as_view(), name="video_play"),

]