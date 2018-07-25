from django.db import models
from datetime import datetime
# Create your models here.

from users.models import UserProfile
from courses.models import Course


# 用户我要学习信息
class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name="姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机")
    course_name = models.CharField(max_length=50, verbose_name="课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name    # 这里很重要，否则在后台就显示不出Meta信息


# 课程评论
class CourseComments(models.Model):
    # 前面知道一个用户发表多个课程评论，所以在课程评论表中将用户设置为外键。
    # 此处的user其实就是一个用来告诉我们这个课程评论属于哪个用户的字段
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户名")
    # 前面知道一门课程具有多个课程评论，所以在课程评论表中将课程设置为外键。
    # 此处的course其实就是一个用来告诉我们这个课程评论属于哪个课程的字段
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    comment = models.CharField(max_length=200, verbose_name="评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comment   # 这里很重要，否则在后台就显示不出Meta信息


# 用户收藏信息
class UserFavorite(models.Model):
    # 前面知道一个用户可以收藏多个内容，所以在用户收藏表中将用户设置为外键。
    # 此处的user其实就是一个用来告诉我们这个用户收藏属于哪个用户的字段
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户名")
    fav_id = models.IntegerField(default=0, verbose_name='数据Id')
    fav_type = models.CharField(choices=(('1', '课程'), ('2', '课程机构'), ('3', '讲师')), default=1, verbose_name='收藏类型',max_length=2)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user   # 这里很重要，否则在后台就显示不出Meta信息


# 用户消息信息
class UserMessage(models.Model):
    # 我们的消息有两种:一种是发给全员，另一种则是发给特定某一个用户。
    # 所以如果使用外键，那么每个消息就要对应一个用户，比较难以实现全员消息的通知。
    # 因此我们设置用户id,如果为0就发给所有用户，不为0就是发给特定Id的用户。
    user = models.IntegerField(default=0, verbose_name="接收用户")
    message = models.CharField(max_length=500, verbose_name='消息内容')
    # 设置消息是否已读，采用布尔类型 BooleanField： False表示未读,True表示已读。
    has_read = models.BooleanField(default=False, verbose_name='是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message  # 这里很重要，否则在后台就显示不出Meta信息


# 用户课程信息
class UserCourse(models.Model):
    # 前面知道一个用户可以学习多门课程，所以在用户课程表中将用户设置为外键。
    # 此处的user其实就是一个用来告诉我们这个课程属于哪个用户的字段
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户名')
    # 前面知道一门课程可以有多个课程的信息，所以在用户课程表中将课程设置为外键。
    # 此处的course其实就是一个用来告诉我们这个课程信息属于哪门课程的字段
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='学习时间')

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name

        def __str__(self):
            return self.user  # 这里很重要，否则在后台就显示不出Meta信息

