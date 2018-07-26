#！/user/bin/python
# -*- coding:utf-8 -*-
# @Time: 2018/7/26 10:05
# @Author: Envse
# @File: adminx.py


import xadmin
# 创建xadmin的全局管理器并与view进行绑定
from xadmin import views
# 因为处于同一个目录之下，所以可以直接使用.models代替当前目录
from .models import EmailVerifyRecord
from .models import Banner
from users.models import EmailVerifyRecord, Banner, UserProfile
from courses.models import Course, CourseResource, Lesson, Video
from organization.models import CourseOrg, CityDict, Teacher
from operation.models import CourseComments, UserMessage, UserFavorite, UserCourse, UserAsk
from django.contrib.auth.models import Group, Permission
from xadmin.models import Log


class BaseSetting(object):
    enable_themes = True  # 修改主题
    use_bootswatch = True    # 增加主题的可选内容


# 写一个管理器，命名规则：Model+Admin,注意这里不再是继承admin，而是继承object这个最高类
class EmailVerifyRecordAdmin(object):
    # 配置后台显示的列信息
    list_display = ['code', 'email', 'send_type', 'send_time']  # 一次显示你想出现的多行数据
    search_fields = ['code', 'email', 'send_type']  # 查询你想要的数据
    list_filter = ['code', 'email', 'send_type', 'send_time']  # 过滤器


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']  # 一次显示你想出现的多行数据
    search_fields = ['title', 'image', 'url', 'index']  # 查询你想要的数据
    list_filter = ['title', 'image', 'url', 'index', 'add_time']  # 过滤器


class GlobalSettings(object):
    site_title = '慕学后台管理系统'
    site_footer = '慕海学习网'
    menu_style = 'accordion'

    def get_site_menu(self):
        return (
                {'title': '课程管理', 'menus': (
                    {'title': '课程信息', 'url': self.get_model_url(Course, 'changelist')},
                    {'title': '章节信息', 'url': self.get_model_url(Lesson, 'changelist')},
                    {'title': '视频信息', 'url': self.get_model_url(Video, 'changelist')},
                    {'title': '课程资源', 'url': self.get_model_url(CourseResource, 'changelist')},
                    {'title': '课程评论', 'url': self.get_model_url(CourseComments, 'changelist')},
                )},
                {'title': '机构管理', 'menus': (
                    {'title': '所在城市', 'url': self.get_model_url(CityDict, 'changelist')},
                    {'title': '机构讲师', 'url': self.get_model_url(Teacher, 'changelist')},
                    {'title': '机构信息', 'url': self.get_model_url(CourseOrg, 'changelist')},
                )},
                {'title': '用户管理', 'menus': (
                    {'title': '用户信息', 'url': self.get_model_url(UserProfile, 'changelist')},
                    {'title': '用户验证', 'url': self.get_model_url(EmailVerifyRecord, 'changelist')},
                    {'title': '用户课程', 'url': self.get_model_url(UserCourse, 'changelist')},
                    {'title': '用户收藏', 'url': self.get_model_url(UserFavorite, 'changelist')},
                    {'title': '用户消息', 'url': self.get_model_url(UserMessage, 'changelist')},
                )},

                {'title': '系统管理', 'menus': (
                    {'title': '用户咨询', 'url': self.get_model_url(UserAsk, 'changelist')},
                    {'title': '首页轮播', 'url': self.get_model_url(Banner, 'changelist')},
                    {'title': '用户分组', 'url': self.get_model_url(Group, 'changelist')},
                    {'title': '用户权限', 'url': self.get_model_url(Permission, 'changelist')},
                    {'title': '日志记录', 'url': self.get_model_url(Log, 'changelist')},
            )},)


# 将EmailVerifyRecord注册进我们的admin中, 并为它选择管理器EmailVerifyRecordAdmin
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
# 将全局配置管理与view进行绑定注册
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)








