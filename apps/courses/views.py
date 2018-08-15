from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.
from .models import Course, CourseResource, Video
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite, CourseComments, UserCourse
from django.http import HttpResponse
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q


# 课程列表页
class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")

        # 热门课程推荐
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 搜索功能
        search_keywords =  request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)| Q(desc__icontains=search_keywords)| Q(detail__icontains=search_keywords))

        # 最热门和参与人数排名
        # 最热门hot根据点击数来判断
        # 参与人数是根据学习人数来判断
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 对课程进行分页,尝试获取前端get请求传递过来的page参数
        # 如果是不合法的配置参数则默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从all_courses中取出来，每页显示9个
        p = Paginator(all_courses, 9, request=request)

        courses = p.page(page)
        return render(request, "course-list.html", {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses,
            "search_keywords": search_keywords,
        })


# 课程详情页
class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 课程点击数增加
        course.click_nums += 1
        course.save()

        # 是否收藏课程，默认为否
        has_fav_course = False
        has_fav_org = False

        # 用户必须已登录我们才判断，否则不需要
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # 相关课程推荐
        tag = course.tag
        if tag:
            # #  这里必须从1开始不然会推荐自己，也就是索引0
            relate_courses = Course.objects.filter(tag=tag)[1:2]
        else:
            relate_courses = []
        return render(request, "course-detail.html", {
            "course": course,
            "relate_courses": relate_courses,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
        })


# 课程章节信息
class CourseInfoView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)

        # 查询用户是否已经开始学习了该课程，如果没有则开始学习
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            course.students += 1
            course.save()
            user_course.save()

        # 取出所有选过这门课的学生
        user_courses = UserCourse.objects.filter(course=course)
        # 取出所有选过这门课的学生的id,采用递归表达式形式
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取出刚才那些学生选过的所有的课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出刚才那些学生选过的所有的课程的id,同样采用递归表达式形式
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        # 取出学过该课程用户学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        return render(request, "course-video.html", {
            "course": course,
            "all_resources": all_resources,
            "relate_courses": relate_courses,
        })


# 课程评论页面
class CourseCommentView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()
        return render(request, "course-comment.html", {
            "course": course,
            "all_resources": all_resources,
            "all_comments": all_comments,
        })


# 用户增加课程评论
class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            # 未登录时页面提示未登录，并跳转到登录页面
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", '')
        if int(course_id) >0 and comments:
            course_comments = CourseComments()
            # get方法只能取出一条数据，如果有多条则抛出异常而且没有数据也抛异常
            # filter方法可以取一个列表出来（可以遍历的queryset），没有数据返回空的queryset，是不会抛异常的
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comment = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')


# 视频播放页面
class VideoPlayView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        all_resources = CourseResource.objects.filter(course=course)
        # 查询用户是否已经开始学习了该课程，如果没有则开始学习
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            course.students += 1
            course.save()
            user_course.save()

        # 取出所有选过这门课的学生
        user_courses = UserCourse.objects.filter(course=course)
        # 取出所有选过这门课的学生的id,采用递归表达式形式
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取出刚才那些学生选过的所有的课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出刚才那些学生选过的所有的课程的id,同样采用递归表达式形式
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        # 取出学过该课程用户学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        return render(request, "course-play.html", {
            "course": course,
            "all_resources": all_resources,
            "relate_courses": relate_courses,
            "video": video,
        })
