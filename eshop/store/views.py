from django.shortcuts import render
from django.views import View
from store.models import *
from django.http import HttpResponse, JsonResponse
from store.util import *
import hashlib


class RegisterView(View):
    """注册"""

    def get(self, request):
        return render(request, 'store/register.html')

    def post(self, request):
        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()
        seller = Seller()
        seller.username = username
        seller.password = set_password(password)
        seller.save()
        return HttpResponse('注册成功')


class LoginView(View):
    """登录"""

    def get(self, request):
        return render(request, 'store/login.html')

    def post(self, request):
        # 获取参数
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        # 查询
        seller = Seller.objects.filter(username=username, password=set_password(password)).first()
        # 判断
        if seller:
            # 保存session
            request.session['logined'] = seller.id
            # 响应
            return HttpResponse('登录成功')
        else:
            # 响应
            return HttpResponse('登录失败')


class BaseView(View):
    """模板页"""

    def get(self, request):
        return render(request, 'store/base.html')


class IndexView(View):
    """首页"""

    def get(self, request):
        return render(request, 'store/index.html')
