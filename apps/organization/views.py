from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.
from .models import CityDict, CourseOrg
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from operation.forms import AnotherUserAskForm


# 课程机构列表功能
class OrgView(View):
    def get(self, request):
        # 查找所有的城市信息
        all_citys = CityDict.objects.all()
        # 查找所有的课程机构信息
        all_orgs = CourseOrg.objects.all()

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


