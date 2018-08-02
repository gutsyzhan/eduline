from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord
from django.db.models import Q
from django.views.generic import View
from users.forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from django.contrib.auth.hashers import make_password
from users.utils.email_send import send_register_eamil


# 用于实现用户注册的函数
class RegisterView(View):
    # get方法直接返回页面
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        # 类的实例化需要一个字典dict参数，而前面我们就知道request.POST是一个QueryDict，所以可以直接传入POST中的信息
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                # register_form回填信息必须有，msg是信息提示
                return render(request, 'register.html', {'register_form': register_form}, {'msg': '该邮箱已被注册过了'})
            else:
                # password为前端页面name的返回值，取到用户名和密码我们就开始进行登录验证;取不到时为空。
                pass_word = request.POST.get("password", "")
                # 实例化一个user_profile对象，存入前端页面获取的值
                user_profile = UserProfile()
                user_profile.username = user_name
                user_profile.email = user_name

                # 默认激活状态为False，也就是未激活
                user_profile.is_active = False

                # 对password进行加密并保存
                user_profile.password = make_password(pass_word)
                user_profile.save()
                send_register_eamil(user_name, 'register')
                pass


# 用于实现用户激活操作的函数
class ActiveUserView(View):
    def get(self, request, active_code):
        # 用于查询邮箱验证码是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的用户
                user = UserProfile.objects.filter(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        # 激活成功跳转到登录页面
        return render(request, "login.html")


# 用于实现用户忘记密码（找回密码）的函数
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            # 发送找回密码的邮件
            send_register_eamil(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, "forgetpwd.html", {'forget_form': forget_form})


# 用于实现用户重置密码的函数
class ResetView(View):
    def get(self, request, active_code):
        # 用于查询邮箱验证码是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的用户
                return render(request, "password_reset.html", {"email": email})   # 告诉页面是哪个用户在重置密码
        else:
            return render(request, "active_fail.html")
        # 激活成功跳转到登录页面
        return render(request, "login.html")


# 用于实现用户修改密码的函数
class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", '')
            pwd2 = request.POST.get("password2", '')
            email = request.POST.get("email", '')
            # 如果前后两次密码不相等，那么回填信息并返回错误提示
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "对不起，前后密码不一致"})
            # 如果前后两次密码相等，那么进入我们的密码修改保存
            # 取出用户信息
            user = UserProfile.objects.get(email=email)
            # 随意取出一个密码并将其进行加密
            user.password = make_password(pwd1)
            # 将更新后的用户信息保存到数据库里面
            user.save()
            # 密码重置成功以后，跳转到登录页面
            return render(request, "login.html", {"msg": "恭喜您，您的密码修改成功，请登录"})
        else:
            email = request.POST.get("email", '')
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})






# # 基于视图函数的实现用户的登录
# # 当我们配置的url被这个view处理时，将会自动传入request对象.
# def user_login(request):
#     # 前端向后端发送的请求方式有两种: get和post
#
#     # 登录提交表单时为post
#     if request.method == "POST":
#         # username，password为前端页面name的返回值，取到用户名和密码我们就开始进行登录验证;取不到时为空。
#         user_name = request.POST.get('username', '')
#         pass_word = request.POST.get('password', '')
#         # 取值成功返回user对象,失败返回null
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             # login 有两个参数：request和user。我们在请求的时候，request实际上是写进了一部分信息，然后在render的时候，这些信息也被返回前端页面从而完成用户登录。
#             login(request, user)
#             # 页面跳转至网站首页 user request也会被带回到首页，显示登录状态
#             return render(request, 'index.html')
#         else:
#             # 说明里面的值是None，再次跳转回主页面并报错
#             return render(request, "login.html", {'msg': '用户名或者密码错误！'})
#     # 获取登录页面时为get
#     elif request.method == "GET":
#         # render的作用是渲染html并返回给用户
#         # render三要素: request ，模板名称 ，一个字典用于传给前端并在页面显示
#         return render(request, "login.html", {})


#  基于类实现用户的登录，它需要继承view
class LoginView(View):
    # 不需要判断，直接调用get方法,因为是获取信息，故这里不需要验证
    def get(self, request):
        # render的作用是渲染html并返回给用户
        # render三要素: request ，模板名称 ，一个字典用于传给前端并在页面显示
        return render(request, "login.html", {})

    # 不需要判断，直接调用post方法
    def post(self, request):
        # 类的实例化需要一个字典dict参数，而前面我们就知道request.POST是一个QueryDict，所以可以直接传入POST中的username，password等信息
        login_form = LoginForm(request.POST)
        # is_valid()方法，用来判断我们所填写的字段信息是否满足我们在LoginForm中所规定的要求，验证成功则继续进行，失败就跳回login页面并重新输入信息
        if login_form.is_valid():
            # username，password为前端页面name的返回值，取到用户名和密码我们就开始进行登录验证;取不到时为空。
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            # 取值成功返回user对象,失败返回null
            user = authenticate(username=user_name, password=pass_word)

            if user is not None:
                if user.is_active:
                    # login 有两个参数：request和user。我们在请求的时候，request实际上是写进了一部分信息，然后在render的时候，这些信息也被返回前端页面从而完成用户登录
                    login(request, user)
                    # 页面跳转至网站首页 user request也会被带回到首页，显示登录状态
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {'msg': '用户未激活！'})
            else:
                # 说明里面的值是None，再次跳转回主页面并报错，这里仅当用户密码出错时才返回
                return render(request, "login.html", {'msg': '用户名或者密码错误！'})
        # 所填写的字段信息不满足我们在LoginForm中所规定的要求，验证失败跳回login页面并重新输入信息
        else:
            return render(request, "login.html", {"login_form": login_form})


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


