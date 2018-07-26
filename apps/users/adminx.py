#！/user/bin/python
# -*- coding:utf-8 -*-
# @Time: 2018/7/26 10:05
# @Author: Envse
# @File: adminx.py


from extra_apps import xadmin
# 因为处于同一个目录之下，所以可以直接使用.models代替当前目录
from .models import EmailVerifyRecord
from .models import Banner


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


# 将EmailVerifyRecord注册进我们的admin中, 并为它选择管理器EmailVerifyRecordAdmin
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)




