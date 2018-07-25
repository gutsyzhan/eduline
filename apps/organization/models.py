from django.db import models
from datetime import datetime
# Create your models here.


# 城市信息
class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name="城市")
    # 描述这一块，我们先用TextField，因为它允许我们不输入长度,而且可以输入值无范围，之后再更新为富文本形式
    desc = models.CharField(max_length=200, verbose_name="描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name   # 这里很重要，否则在后台就显示不出Meta信息


# 课程机构
class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name="机构名称")
    desc = models.TextField(verbose_name="机构描述")
    tag = models.CharField(max_length=10, default="全国知名", verbose_name="机构标签")
    category = models.CharField(max_length=20, default='pxjg', choices=(('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高校')), verbose_name="机构类别")
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(max_length=50, upload_to="org/%Y/%m", verbose_name="logo")
    address = models.CharField(max_length=150, verbose_name="机构地址")
    # 前面知道一个城市对应多个课程机构，所以在课程机构表中将城市设置为外键。
    # 此处的city其实就是一个用来告诉我们这个课程机构属于哪个城市的字段
    city = models.ForeignKey(CityDict, on_delete=models.CASCADE, verbose_name="所在城市说明")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    course_nums = models.IntegerField(default=0, verbose_name="课程数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name   # 这里很重要，否则在后台就显示不出Meta信息


# 教师信息
class Teacher(models.Model):
    # 前面知道一个课程机构对应多个教师，所以在教师信息表中将授课机构设置为外键。
    # 此处的org其实就是一个用来告诉我们这个教师属于哪个课程机构的字段
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属教师")
    name = models.CharField(max_length=50, verbose_name="教师名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_position = models.CharField(max_length=50, verbose_name="公司职位")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    points = models.CharField(max_length=50, verbose_name="教学特点")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    age = models.IntegerField(default=18, verbose_name='年龄')
    image = models.ImageField(default='', upload_to='teacher/%Y/%m', verbose_name='头像', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name   # 这里很重要，否则在后台就显示不出Meta信息

