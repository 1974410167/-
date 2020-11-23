from django.shortcuts import render,reverse,redirect
from django.http import HttpResponse
from django.views import View
from .models import User,CourseMessage

from .stu_sign.cookie import generate_Cookies
from .stu_sign.util import util_1
from .stu_sign.main import get_headers


def index(request):

    return render(request,'index.html')


class login(View):

    template_html = 'login.html'
    message = ''

    def get(self,request):

        # 判断是否已经登录
        if request.session.get('is_login'):
            account = request.session.get('account')
            print(account)
            return redirect(reverse('app1:center_url',args=(account,)))

        return render(request,self.template_html)

    def post(self,request):

        account = request.POST.get('account')
        password = request.POST.get('password')

        obj = User.objects.filter(account=account)

        if obj:
            obj_password = obj[0].password
            if obj_password == password:

                request.session['is_login'] = True
                request.session['account'] = account

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

            # 用户实例
            t = User()
            t.account = account
            t.password = password
            t.email = email
            t.uid = uid
            t.save()

            course_list = obj_uid.get_mycourse_list()

            for item in course_list:
                courseid = item['courseid']
                classid = item['classid']
                coursename = item['name']
                teacherfactor = item['teacherfactor']

                # 查看课程是否已经存在数据库
                obj_data = CourseMessage.objects.filter(courseid=courseid,classid=classid,coursename=coursename,teacherfactor=teacherfactor)

                # 若存在，直接添加到用户课程

                if obj_data:
                    t.course_message.add(obj_data[0])

                # 不存在创建，创建课程，并且保存
                else:

                    a = CourseMessage()
                    a.courseid = courseid
                    a.classid = classid
                    a.coursename = coursename
                    a.teacherfactor = teacherfactor
                    a.save()

                    t.course_message.add(a)

            return redirect(reverse('app1:login_url'))

        else:
            self.message = '账号或密码错误'
            return render(request, self.template_html, {'message': self.message})

class personal_center(View):

    def get(self,request,account):

        if request.session.get('is_login'):
            user = User.objects.filter(account=account)
            if user:
                # 如果在数据库中存在此用户，获得此用户的课程列表
                course_message_list = user[0].course_message.all()

                # 获得活跃课程列表,字典形式
                is_activates_list = user[0].is_activates

                # 获得课程id,对每一个学生来说，他的课程id唯一
                course_id_list = is_activates_list.keys()

            else:
                message = '你的账号不存在，请注册'
                return render(request,"register.html",{'message':message})

            context = {
                "course_message_list": course_message_list,
                "course_id_list": course_id_list,
                'account':account
            }

            return render(request,'person_center.html',context=context)
        else:
            return HttpResponse('未登录')

class quit_center(View):

    def get(self,request):

        request.session.flush()

        return render(request,'index.html')

class handle(View):

    def get(self,request):

        return HttpResponse('Get请求无效')

    def post(self,request):

        account = request.POST.get('account')
        status_code = request.POST.get('status_code')
        courseid = request.POST.get('courseid')

        query_user = User.objects.filter(account=account)
        # 存数据
        if status_code == "1":
            if query_user:
                user_dict = query_user[0].is_activates

                uid = query_user[0].uid
                course = query_user[0].course_message.filter(courseid=courseid)

                if course:
                    classid = course[0].classid
                    teacherfactor = course[0].teacherfactor
                    coursename = course[0].coursename

                    user_dict[courseid] = {
                        'uid':uid,
                        'courseid': courseid,
                        'classid': classid,
                        'teacherfactor': teacherfactor,
                        'coursename': coursename,
                    }

                    query_user[0].save()

                    res = HttpResponse()
                    res.status_code = 200

                    return res

            return render(request,'login.html')

        if status_code == "0":

            if query_user:
                user_dict = query_user[0].is_activates

                user_dict.pop(courseid)
                query_user[0].save()

                res = HttpResponse()
                res.status_code = 200
                return res

            return render(request,'login.html')









