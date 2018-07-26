from django.contrib import admin

# Register your models here.
# 因为处于同一个目录之下，所以可以直接使用.models代替当前目录
from .models import UserProfile


# 写一个管理器，命名规则：Model+Admin
class UserProfileAdmin(admin.ModelAdmin):
    pass


# 将UserProfile注册进我们的admin中, 并为它选择管理器UserProfileAdmin
admin.site.register(UserProfile, UserProfileAdmin)

