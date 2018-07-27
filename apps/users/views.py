from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile
from django.db.models import Q


# 当我们配置的url被这个view处理时，将会自动传入request对象.
def user_login(request):
    # 前端向后端发送的请求方式有两种: get和post

    # 登录提交表单时为post
    if request.method == "POST":
        # username，password为前端页面name的返回值，取到用户名和密码我们就开始进行登录验证;取不到时为空。
        user_name = request.POST.get('username', '')
        pass_word = request.POST.get('password', '')
        # 取值成功返回user对象,失败返回null
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            # login 有两个参数：request和user。我们在请求的时候，request实际上是写进了一部分信息，然后在render的时候，这些信息也被返回前端页面从而完成用户登录。
            login(request, user)
            # 页面跳转至网站首页 user request也会被带回到首页，显示登录状态
            return render(request, 'index.html')
        else:
            # 说明里面的值是None，再次跳转回主页面并报错
            return render(request, "login.html", {'msg': '用户名或者密码错误！'})
    # 获取登录页面时为get
    elif request.method == "GET":
        # render的作用是渲染html并返回给用户
        # render三要素: request ，模板名称 ，一个字典用于传给前端并在页面显示
        return render(request, "login.html", {})


# 用于实现邮箱登录的函数
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 我们不希望用户存在两个，也就是说通过某个用户名和某个邮箱登录的都是指向同一用户，所以采用Q来进行并集查询
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))

            # 记住不能使用password==password，因为密码都被django的后台给加密了

            # UserProfile继承的AbstractUser中有check_password这个函数
            if user.check_password(password):
                return user
        except Exception as e:
            return None

