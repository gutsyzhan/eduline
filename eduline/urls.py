"""eduline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.views.generic import TemplateView
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
from organization.views import OrgView
from eduline.settings import MEDIA_ROOT
import xadmin


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # 用''指代根目录，TemplateView.as_view可以将template转换为view
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    # 登录url
    # path('login/', TemplateView.as_view(template_name="login.html"), name="login")
    # path('login/', user_login, name="login")
    path('login/', LoginView.as_view(), name="login"),
    # 注册url
    path("register/", RegisterView.as_view(), name="register"),

    # 验证码url
    path("captcha/", include('captcha.urls')),
    # 激活用户url
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name="user_active"),
    # 找回密码url
    path("forget/", ForgetPwdView.as_view(), name="forget_pwd"),

    # 密码重置url
    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name="reset_pwd"),

    # 修改密码url
    path("modify/", ModifyPwdView.as_view(), name="modify_pwd"),

    # 课程机构应用path配置
    path("org/", include('organization.urls', namespace="org")),

    # 配置文件上传的访问处理url
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    # 课程相关应用path配置
    path("course/", include('courses.urls', namespace="course")),


]

