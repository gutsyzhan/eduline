#！/user/bin/python
# -*- coding:utf-8 -*-
# @Time: 2018/7/26 14:37
# @Author: Envse
# @File: adminx.py

import xadmin

from .models import Course, Lesson, Video, CourseResource, BannerCourse


# 课程直接添加章节
class LessonInline(object):
    model = Lesson
    extra = 0


# 课程直接添加章课程资源
class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                    'add_time', 'get_zj_nums', 'go_to']  # 一次显示你想出现的多行数据
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image',
                     'click_nums']  # 查询你想要的数据
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                   'add_time']  # 过滤器
    # # 默认排序：以点击数排序
    # ordering = ['-click_nums']
    #
    # # 字段只读：点击数只允许读取
    # readonly_fields = ['click_nums', 'fav_nums']
    #
    # # 字段隐藏：收藏数隐藏显示
    # exclude = ['fav_nums']
    # # 注意字段只读和字段隐藏是冲突的，不允许设置一个字段只读同时隐藏

    # 课程直接添加章节,课程资源
    inlines = [LessonInline, CourseResourceInline]

    # 直接列表页编辑
    list_editable = ['degree', 'desc', ]

    # # 列表页定时刷新
    # refresh_times = [3, 5]

    # 过滤列表中的数据
    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    # 字段联动功能
    def save_models(self):
        # 在保存课程的时候,统计课程机构的课程数
        obj = self.new_obj
        # 新增课程还没有保存，统计的课程数就会少一个
        obj.save()
        # 必须确定存在
        if obj.course_org is not None:
            # obj实际是一个course对象
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                    'add_time', 'get_zj_nums', 'go_to']  # 一次显示你想出现的多行数据
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image',
                     'click_nums']  # 查询你想要的数据
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                   'add_time']  # 过滤器
    # # 默认排序：以点击数排序
    # ordering = ['-click_nums']
    #
    # # 字段只读：点击数只允许读取
    # readonly_fields = ['click_nums', 'fav_nums']
    #
    # # 字段隐藏：收藏数隐藏显示
    # exclude = ['fav_nums']
    # # 注意字段只读和字段隐藏是冲突的，不允许设置一个字段只读同时隐藏

    # 课程直接添加章节,课程资源
    inlines = [LessonInline, CourseResourceInline]

    # 过滤列表中的数据
    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


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
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideosAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)