#！/user/bin/python
# -*- coding:utf-8 -*-
# @Time: 2018/8/14 15:58
# @Author: Envse
# @File: urls.py


from django.urls import path, include, re_path
from .views import UserInfoView, ImageUploadView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourseView
from .views import MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

app_name = "users"

urlpatterns = [
    # 用户信息页url
    path("info/", UserInfoView .as_view(), name="user_info"),

    # 用户个人中心修改头像url
    path("image/upload/", ImageUploadView .as_view(), name="image_upload"),

    # 用户个人中心修改密码url
    path("update/pwd/", UpdatePwdView.as_view(), name="update_pwd"),

    # 用户个人中心发送邮箱验证码url
    path("sendemail_code/", SendEmailCodeView.as_view(), name="sendemail_code"),

    # 用户个人中心修改邮箱url
    path("update_email/", UpdateEmailView.as_view(), name="update_email"),

    # 用户个人中心我的课程url
    path("mycourse/", MyCourseView.as_view(), name="mycourse"),

    # 我收藏的课程机构url
    path("myfav/org/", MyFavOrgView.as_view(), name="myfav_org"),

    # 我收藏的授课讲师url
    path("myfav/teacher/", MyFavTeacherView.as_view(), name="myfav_teacher"),

    # 我收藏的公开课程url
    path("myfav/course/", MyFavCourseView.as_view(), name="myfav_course"),

    # 我的消息url
    path("mymessage/", MyMessageView.as_view(), name="mymessage"),



]