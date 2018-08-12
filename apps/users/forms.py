#！/user/bin/python
# -*- coding:utf-8 -*-
# @Time: 2018/7/30 10:36
# @Author: Envse
# @File: forms.py

from django import forms
from captcha.fields import CaptchaField   # 引入验证码field


# 用户登录表单的验证，注意字段与前端页面保持一致
class LoginForm(forms.Form):
    username = forms.CharField(required=True)  # 用户名不能为空
    password = forms.CharField(required=True, min_length=5)  # 密码不能为空，而且最小5位数


# 用户登录表单时验证码的验证，注意字段与前端页面保持一致
class RegisterForm(forms.Form):
    email = forms.CharField(required=True)  # 用户名不能为空
    password = forms.CharField(required=True, min_length=5)  # 密码不能为空，而且最小5位数
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


# 用户找回密码时的表单，注意字段与前端页面保持一致
class ForgetForm(forms.Form):
    email = forms.CharField(required=True)  # 用户名不能为空
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


# 用户修改密码时的表单，注意字段与前端页面保持一致
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)  # 新密码不能为空
    password2 = forms.CharField(required=True, min_length=5)  # 确认密码不能为空


# 激活时验证码实现
class ActiveForm(forms.Form):
    # 激活时不需要对邮箱的密码做验证
    # 应用验证码，自定义错误输出key必须与异常一样
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})