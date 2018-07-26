#！/user/bin/python
# -*- coding:utf-8 -*-
# @Time: 2018/7/26 14:37
# @Author: Envse
# @File: adminx.py

import xadmin

from .models import Course, Lesson, Video, CourseResource


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                    'add_time']  # 一次显示你想出现的多行数据
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image',
                     'click_nums']  # 查询你想要的数据
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                   'add_time']  # 过滤器


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']  # 一次显示你想出现的多行数据
    search_fields = ['course', 'name']  # 查询你想要的数据
    list_filter = ['course__name', 'name', 'add_time']  # 过滤器,__name是外键的name字段，只写course则无法在过滤器中显示。


class VideosAdmin(object):
    list_display = ['lesson', 'name', 'add_time']  # 一次显示你想出现的多行数据
    search_fields = ['lesson', 'name']  # 查询你想要的数据
    list_filter = ['lesson', 'name', 'add_time']  # 过滤器,__name是外键的name字段，只写course则无法在过滤器中显示。


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']  # 一次显示你想出现的多行数据
    search_fields = ['course', 'name', 'download']  # 查询你想要的数据
    list_filter = ['course', 'name', 'download', 'add_time']  # 过滤器,__name是外键的name字段，只写course则无法在过滤器中显示。


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideosAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)