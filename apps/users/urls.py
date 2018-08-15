#！/user/bin/python
# -*- coding:utf-8 -*-
# @Time: 2018/8/14 15:58
# @Author: Envse
# @File: urls.py


from django.urls import path, include, re_path
from .views import UserInfoView, ImageUploadView, UpdatePwdView, SendEmailCodeView, UpdateEmailView


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

]