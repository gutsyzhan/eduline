from django.db import models
from datetime import datetime
# Create your models here.
from organization.models import CourseOrg, Teacher


# 课程信息
class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,  on_delete=models.CASCADE, verbose_name="课程机构", null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="讲师", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="课程名")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    detail = models.TextField(max_length=500, verbose_name="课程详情")
    is_banner = models.BooleanField(default=False, verbose_name="是否轮播")
    degree = models.CharField(max_length=2, choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), verbose_name="难度等级")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长（分钟数）")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to='courses/%Y/%m', max_length=100, verbose_name="封面图片")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    category = models.CharField(default="后端开发", max_length=20, verbose_name="课程类别")
    tag = models.CharField(default='', max_length=10, verbose_name="课程标签")
    youneeded_know = models.CharField(default='', max_length=300, verbose_name="课程须知")
    teacher_tell = models.CharField(default='', max_length=300, verbose_name="老师告诉你")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "普通课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获取课程章节数
        return self.lesson_set.all().count()
    get_zj_nums.short_description = "章节数"

    def go_to(self):
        from django.utils.safestring import mark_safe
        # 如果不使用mark_safe，系统则会对其进行转义
        return mark_safe("<a href='http://blog.licheetools.top'>跳转</>")
    go_to.short_description = "跳转"

    def get_learn_users(self):
        # 获取学习用户数
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        # 获取课程所有章节
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name = "轮播课程"
        verbose_name_plural = verbose_name
        proxy = True  # 很重要，否则会生成另外一张表，这样设置具有model的功能，但不会生成表


# 章节信息
class Lesson(models.Model):
    # 前面知道一个课程对应多个章节，所以在章节表中将课程设置为外键。
    # 此处的course其实就是一个用来告诉我们这个章节属于哪个课程的字段
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<<{0}>>课程的章节》{1}'.format(self.course, self.name)   # return self.name也是可以的

    def get_lesson_video(self):
        # 获取章节视频信息
        return self.video_set.all()


# 视频信息
class Video(models.Model):
    # 前面知道一个章节对应多个视频，所以在视频表中将章节设置为外键。
    # 此处的lesson其实就是一个用来告诉我们这个视频属于哪个章节的字段
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="章节")
    name = models.CharField(max_length=100, verbose_name="视频名称")
    url = models.URLField(max_length=200, default='', verbose_name="访问地址")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长（分钟数）")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<<{0}>>章节的视频》{1}'.format(self.lesson, self.name)   # return self.name也是可以


# 课程资料信息
class CourseResource(models.Model):
    # 前面知道一个课程对应多个课程资料，所以在课程资料表中将课程设置为外键。
    # 此处的course其实就是一个用来告诉我们这个课程资料属于哪个课程的字段
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="名称")
    download = models.FileField(max_length=100, upload_to='course/resource/%Y/%m', verbose_name="资源文件")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<<{0}>>课程的课程资料》{1}'.format(self.course, self.name)   # return self.name也是可以

