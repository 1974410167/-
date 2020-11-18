from django.shortcuts import render,reverse,get_object_or_404,redirect,Http404
from django.http import HttpResponse,request
from django.views import View
from .models import User,CourseMessage

from .stu_sign.cookie import generate_Cookies
from .stu_sign.util import util_1
from .stu_sign.main import get_headers

a = CourseMessage()
a.courseid = '1234'
a.classid = '2345'
a.coursename = '数学'
a.teacherfactor = '大黄'
a.save()


def index(request):

    s = '<h1>success</h1>'
    name = 'hello world sss'
    return render(request,'index.html',context={"name":name})

def login(request):

    s = '<h1>success</h1>'
    name = 'hello world sss'
    return render(request,'login.html',context={"name":name})
class login(View):

    template_html = 'login.html'
    message = ''

    def get(self,request):

        # 判断是否已经登录
        if request.session.get('is_login'):
            account = request.session.get('account')
            return redirect(reverse('app1:center_url',args=(account,)))

        return render(request,self.template_html)

    def post(self,request):

        account = request.POST.get('account')
        password = request.POST.get('password')

        obj = User.objects.filter(account=account)
        if obj:
            obj_password = obj.password
            if obj_password == password:
                return redirect(reverse('app1:center_url',args=(account,)))
            else:
                self.message = '密码错误'
                return render(request,self.template_html,{'message':self.message})
        self.message = '账号不存在'
        return render(request, self.template_html, {'message': self.message})



class register(View):

    template_html = 'register.html'
    message = ''

    def get(self,request):

        if request.session.get('is_login'):
            account = request.session.get('account')
            return redirect(reverse('app1:center_url',args=(account,)))

        return render(request,self.template_html)

    def post(self,request):

        account = request.POST.get("account")
        password = request.POST.get('password')
        email = request.POST.get('email')

        # 查看账号是否已经注册
        if User.objects.filter(account=account):
            self.message = '账号已被注册'
            return render(request,self.template_html, {'message':self.message})

        # 查看账号是否能登录学习通
        obj = generate_Cookies(user=account,password=password)
        cookies = obj.get_cookies()
        # 以是否生成指定cookie判断是否登录成功
        if cookies:

            obj_uid = util_1()
            obj_uid.headers = get_headers()
            obj_uid.cookies = cookies
            uid = obj_uid.get_uid()

            t = User()
            t.account = account
            t.password = password
            t.email = email
            t.uid = uid
            t.course_message = a
            t.save()
            self.message = '注册成功，请登录！'
            return render(request, self.template_html, {'message': self.message})

        else:
            self.message = '账号或密码错误'
            return render(request, self.template_html, {'message': self.message})


# def register(request):
#     s = '<h1>success</h1>'
#     name = 'hello world sss'
#     return render(request,'register.html',context={"name":name})


def Personal_center(request,account):


    return HttpResponse(f"<h1>个人中心{account}</h1>")