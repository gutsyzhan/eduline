#！/user/bin/python
# -*- coding:utf-8 -*-
# @Time: 2018/7/26 15:01
# @Author: Envse
# @File: adminx.py

import xadmin


from .models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']  # 一次显示你想出现的多行数据
    search_fields = ['name', 'mobile', 'course_name']  # 查询你想要的数据，记住尽量不要把时间放进去
    list_filter = ['name', 'mobile', 'course_name', 'add_time']  # 过滤器,__name是外键的name字段，只写course则无法在过滤器中显示。


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']  # 一次显示你想出现的多行数据
    search_fields = ['user', 'course', 'comments']  # 查询你想要的数据，记住尽量不要把时间放进去
    list_filter = ['user', 'course', 'comments', 'add_time']  # 过滤器,__name是外键的name字段，只写course则无法在过滤器中显示。


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']  # 一次显示你想出现的多行数据
    search_fields = ['user', 'fav_id', 'fav_type']  # 查询你想要的数据，记住尽量不要把时间放进去
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']  # 过滤器,__name是外键的name字段，只写course则无法在过滤器中显示。


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']  # 一次显示你想出现的多行数据
    search_fields = ['user', 'message', 'has_read']  # 查询你想要的数据，记住尽量不要把时间放进去
    list_filter = ['user', 'message', 'has_read', 'add_time']  # 过滤器,__name是外键的name字段，只写course则无法在过滤器中显示。


class UserCourseAdmin(object):
    list_display = ['user',  'course', 'add_time']  # 一次显示你想出现的多行数据
    search_fields = ['user',  'course']  # 查询你想要的数据，记住尽量不要把时间放进去
    list_filter = ['user',  'course', 'add_time']  # 过滤器,__name是外键的name字段，只写course则无法在过滤器中显示。


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)


