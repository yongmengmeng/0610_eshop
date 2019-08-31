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
from django.contrib.auth import authenticate, login, logout
from store.models import *
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
            username, url, url)  # html内容
        # 发送
        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        # 响应
        return HttpResponse('登录邮箱去激活')


class LoginView(View):
    """登录"""

    def get(self, request):
        # 获取cookie
        username = request.COOKIES.get('username')
        # 响应
        return render(request, 'buyer/login.html',{'username':username})

    def post(self, request):
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        # 校验数据
        if not all([username, password]):
            return render(request, 'buyer/login.html',
                          {'script': 'alert("数据不完整")', 'username': username, 'password': password,
                           'remember': remember})
        # 业务处理:登录校验  登录成返回当前用户对象 登录失败返回None
        user = authenticate(username=username, password=password)
        # 判断用户是否登录成功
        if user:
            # 判断用户是否已激活
            if user.is_active:
                # 记录用户的登录状态
                login(request, user)
                # 获取需要跳转的url
                next_url = request.GET.get('next')
                # 判断是否含有需要回跳的url
                if next_url:
                    response = redirect(next_url)
                else:
                    response = redirect('/buyer/index/')

                # 判断是否需要记住用户名
                if remember == 'on':
                    response.set_cookie('username', username, 60 * 60 * 24 * 7)
                else:
                    response.delete_cookie('username')

                # 响应
                return response
            else:
                # 用户未激活
                return render(request, 'buyer/login.html',
                              {'script': 'alert("账户未激活")', 'username': username, 'password': password,
                               'remember': remember})
        else:
            return render(request, 'buyer/login.html',
                          {'script': 'alert("用户名或密码错误")', 'username': username, 'password': password,
                           'remember': remember})


class IndexView(View):
    """登录"""

    def get(self, request):
        #获取所有商品类型
        list_goodstype = GoodsType.objects.order_by('id')
        #循环，动态添加属性
        for goodstype in list_goodstype:
            goodstype.four = Goods.objects.filter(goodstype=goodstype,up=True).order_by('-productdate')[:4]
            goodstype.three = Goods.objects.filter(goodstype=goodstype,up=True).order_by('-sale')[:3]
        # 响应
        return render(request, 'buyer/index.html',{'list_goodstype':list_goodstype})


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
