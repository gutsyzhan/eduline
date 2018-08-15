from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.
from .models import CityDict, CourseOrg
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from operation.forms import AnotherUserAskForm
from courses.models import Course
from operation.models import UserFavorite
from organization.models import Teacher
from django.db.models import Q


# 课程机构列表功能
class OrgView(View):
    def get(self, request):
        # 查找所有的城市信息
        all_citys = CityDict.objects.all()
        # 查找所有的课程机构信息
        all_orgs = CourseOrg.objects.all()

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # 授课机构的排名
        hot_orgs = all_orgs.order_by("click_nums")[:3]

        # 学习人数和课程人数排名
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        # 城市信息的筛选
        #  取出筛选城市，默认为空
        city_id = request.GET.get('city', '')
        # 选中了某个城市之后，根据城市Id与数据库中的city_id进行判断（外键city在数据库中名为city_id且为字符串类型）
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 机构类别的筛选
        # ct是我们前端页面用于判断机构类别用的
        category = request.GET.get('ct', '')
        # 选中了类别之后，根据category与数据库中的category进行判断，从而显示授课机构
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 统计课程机构的数量
        org_nums = all_orgs.count()

        # 对课程机构进行分页,尝试获取前端get请求传递过来的page参数
        # 如果是不合法的配置参数则默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从all_org中取五个出来，每页显示6个
        p = Paginator(all_orgs, 6, request=request)

        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_citys": all_citys,
            "all_orgs": orgs,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
            "search_keywords": search_keywords,
        })


# 我要学习功能实现
class AddUserAskView(View):
    def post(self, request):
        userask_form = AnotherUserAskForm(request.POST)
        # 判断form是否有效
        if userask_form.is_valid():
            #  注意modelform和form的区别，modelform它有model的属性，而且有个参数commit，当它为真时会把数据存入到数据库
            user_ask = userask_form.save(commit=True)

            # 如果保存成功,则返回json,不过后面必须有content_type用于告诉浏览器返回的类型
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        else:
            # 如果保存失败，则返回json,并将form的错误信息通过msg传递到前端进行显示
            return HttpResponse("{'status': 'fail', 'msg':{0}}".format(userask_form.errors), content_type='application/json')


# 机构首页
class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = "home"
        # 根据id来获取课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 根据取到的课程机构直接获取它的所有课程，我们取3个
        all_courses = course_org.course_set.all()[:3]

        # 根据取到的课程机构直接获取它的所有讲师，我们取1个
        all_teachers = course_org.teacher_set.all()[:1]

        has_fav = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, "org-detail-homepage.html", {
            "all_courses": all_courses,
            "all_teachers": all_teachers,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


# 机构课程列表页
class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = "course"
        # 根据id来获取课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 根据取到的课程机构直接获取它的所有课程
        all_courses = course_org.course_set.all()

        has_fav = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, "org-detail-course.html", {
            "all_courses": all_courses,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


# 机构课程详情页
class OrgDescView(View):
    def get(self, request, org_id):
        current_page = "desc"
        # 根据id来获取课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, "org-detail-desc.html", {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


# 机构讲师列表页
class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = "teachers"
        # 根据id来获取课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 根据取到的课程机构直接获取它的所有讲师
        all_teachers = course_org.teacher_set.all()

        has_fav = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, "org-detail-teachers.html", {
            "course_org": course_org,
            "current_page": current_page,
            "all_teachers": all_teachers,
            "has_fav": has_fav,
        })


# 用户收藏与取消收藏功能
class AddFavView(View):
    def post(self, request):
        # 取出fav_id，尽管是字符串类型，但是我们后面会进行整型转换，所以默认为0
        fav_id = request.POST.get('fav_id', 0)
        # 取到fav_type，尽管是字符串类型，但是我们后面会进行整型转换，所以默认为0
        fav_type = request.POST.get('fav_type', 0)

        # 未收藏时收藏和已收藏时取消收藏
        # 判断用户是否登录，即使用户没有登录会有一个匿名的user
        if not request.user.is_authenticated:
            # 未登录时页面提示未登录，并跳转到登录页面
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在， 那么用户就可以取消收藏
            exist_records.delete()
            # 下面是根据收藏类型来进行删除，同时删除后机构类型对应的喜欢人数也会减一
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                course.save()
                if course.fav_nums <= 0:
                    course.fav_nums = 0
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                course_org.save()
                if course_org.fav_nums <= 0:
                    course_org.fav_nums = 0
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                teacher.save()
                if teacher.fav_nums <= 0:
                    teacher.fav_nums = 0

            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            # 过滤掉未取到fav_id type的默认情况
            if int(fav_type) > 0 and int(fav_id) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                # 下面是根据收藏类型来进行增加，同时增加记录后机构类型对应的喜欢人数也会加一
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


# 课程讲师列表页
class TeacherListView(View):
    def get(self, request):
        # 取出所有的讲师
        all_teachers = Teacher.objects.all()

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords)|
                                               Q(work_position__icontains=search_keywords))

        # 人气排名
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")

        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by("-fav_nums")[:5]

        # 统计课程讲师的数量
        teacher_nums = all_teachers.count()

        # 对课程讲师进行分页,尝试获取前端get请求传递过来的page参数
        # 如果是不合法的配置参数则默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从all_org中取五个出来，每页显示6个
        p = Paginator(all_teachers, 6, request=request)

        teachers = p.page(page)

        return render(request, "teachers-list.html", {
            "all_teachers": teachers,
            "sorted_teacher": sorted_teacher,
            "sort": sort,
            "teacher_nums": teacher_nums,
            "search_keywords": search_keywords,
        })


# 讲师详情页
class TeacherDetailView(View):
    def get(self, request, teacher_id):
        # 取出当前id的讲师信息
        teacher = Teacher.objects.get(id=int(teacher_id))
        # 前面的teacher是数据库里面的字段，后一个则是上面取到的teacher
        all_courses = Course.objects.filter(teacher=teacher)

        has_fav_teacher = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_fav_teacher = True
        has_fav_org = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_fav_org = True

        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by("-fav_nums")[:5]

        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "all_courses": all_courses,
            "sorted_teacher": sorted_teacher,
            "has_fav_teacher": has_fav_teacher,
            "has_fav_org": has_fav_org,
        })

