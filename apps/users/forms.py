#！/user/bin/python
# -*- coding:utf-8 -*-
# @Time: 2018/7/30 10:36
# @Author: Envse
# @File: forms.py

from django import forms


# 用户登录表单的验证
class LoginForm(forms.Form):
    username = forms.CharField(required=True)  # 用户名不能为空
    password = forms.CharField(required=True, min_length=5)  # 密码不能为空，而且最小5位数

