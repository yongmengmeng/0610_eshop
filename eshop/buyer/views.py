from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.views import View
from buyer.models import *
from store.util import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from buyer.util import *
from itsdangerous import SignatureExpired, BadSignature
from django.core.mail import send_mail
import os


class RegisterView(View):
    """注册"""

    def get(self, request):
        # 响应
        return render(request, 'buyer/register.html')

    def post(self, request):
        # 获取参数
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        cpassword = request.POST.get('cpassword').strip()
        email = request.POST.get('email').strip()
        allow = request.POST.get('allow')

        # # 后端判断，为了更安全，大家接着思路实现
        # if not all([username,password,cpassword,email]):
        #     return render(request, 'buyer/register.html', {'script': 'alert("数据必填")'})
        # elif len(username)<5 or len(username)>20:
        #     return render(request, 'buyer/register.html', {'script': 'alert("用户名必须是5-10位")'})

        # 用户认证系统提供的create_user方法，创建用户对象，密码会加密
        buyer = Buyer.objects.create_user(username=username, password=password, email=email)
        # 修改为未激活，为了与后面的邮件激活做准备
        buyer.is_active = False
        buyer.save()

        ################################发邮件################################
        # 准备加密的数据
        data = {'id': buyer.id}
        # 加密
        data = itsdangerous_encrypt(data, settings.SECRET_KEY, 60 * 60 * 24)
        # 拼接url
        url = '{}://{}/buyer/active?data={}'.format(request.scheme, request.get_host(), data)
        # 准备发邮件的参数
        subject = '天天生鲜欢迎信息'  # 主题
        message = ''  # 文本内容
        from_email = settings.EMAIL_FROM  # 发件人
        recipient_list = [buyer.email]  # 收件人
        html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/><a href="%s">%s</a>' % (
            username,url,url)  # html内容
        #发送
        send_mail(subject, message, from_email, recipient_list,html_message=html_message)

        # 响应
        return HttpResponse('登录邮箱去激活')


class LoginView(View):
    """登录"""

    def get(self, request):
        # 响应
        return render(request, 'buyer/login.html')

    def post(self, request):
        # # 获取参数
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # # 创建对象
        # seller = Seller()
        # seller.username = username
        # seller.password = set_password(password)
        # # 新增
        # seller.save()
        # # 响应
        # return redirect('/store/login/')
        return HttpResponse('OK')


class IndexView(View):
    """登录"""

    # @method_decorator(login_required)
    def get(self, request):
        print(dir(request))
        print('*' * 10000)
        print(request.scheme)
        print(request.get_host())
        print(request.get_port())
        # 响应
        return render(request, 'buyer/index.html')


class ActiveView(View):
    """激活"""

    def get(self, request):
        # 获取参数
        data = request.GET.get('data')
        print(data)
        # 解密并异常处理
        try:
            data = itsdangerous_deencrypt(data, settings.SECRET_KEY, 60 * 60 * 24)
        except SignatureExpired:
            return HttpResponse('已过期')
        except BadSignature:
            return HttpResponse('非法操作')
        # 根据id查找用户
        buyer = Buyer.objects.filter(pk=data.get('id')).first()
        # 修改属性
        buyer.is_active = True
        # 修改
        buyer.save()
        # 响应
        return HttpResponse('激活成功')
