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
from store.util import baidu_page
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
        return render(request, 'buyer/login.html', {'username': username})

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
        # 获取所有商品类型
        list_goodstype = GoodsType.objects.order_by('id')
        # 循环 动态添加属性  three属性表示销量最高的商品前3个   four属性表示最新日期的商品前4个
        for goodstype in list_goodstype:
            goodstype.three = Goods.objects.filter(goodstype=goodstype, up=True).order_by('-sale')[:3]
            goodstype.four = Goods.objects.filter(goodstype=goodstype, up=True).order_by('-productdate')[:4]
        # 响应
        return render(request, 'buyer/index.html', {'list_goodstype': list_goodstype})


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


class DetailView(View):
    """详情"""

    def get(self, request):
        # 获取参数
        goods_id = request.GET.get('goods_id')
        # 根据商品id获取商品对象
        goods = Goods.objects.filter(pk=goods_id).first()
        # 查询商品同类型下的最新上架的2个商品
        list_goods = Goods.objects.filter(goodstype=goods.goodstype).order_by('-id')[:2]
        # 响应
        return render(request, 'buyer/detail.html', {'goods': goods, 'list_goods': list_goods})


class ListView(View):
    """列表页"""

    def get(self, request):
        ###################################获取参数###################################
        # 商品类型id
        goodstype_id = request.GET.get('goodstype_id')
        # 排序方式
        sort = request.GET.get('sort')
        # 搜索关键词
        # key_word = request.GET.get('key_word')
        # if not key_word:
        #     key_word = ''
        # 页码
        page_now = request.GET.get('page_now')
        ###################################判断排序方式###################################
        if not sort:
            sort = '0'
        ##################################判断处理页码####################################
        if not page_now:
            page_now = 1
        page_now = int(page_now)
        ##################################根据排序方式获取结果集####################################
        # 根据id获取对象
        goodstype = GoodsType.objects.filter(pk=goodstype_id).first()
        # 判断排序方式，根据不同的排序方式获取对应的用于分页的结果集 '0': 按照id倒叙  '1': 按照价格  '2': 按照销量人气
        if sort == '1':
            qs_goods = Goods.objects.filter(goodstype=goodstype).order_by('price')
        elif sort == '2':
            qs_goods = Goods.objects.filter(goodstype=goodstype).order_by('-sale')
        else:
            qs_goods = Goods.objects.filter(goodstype=goodstype).order_by('id')
        ##################################分页相关####################################
        # 设置每页显示的数据的数量
        page_size = 10
        # 创建分页对象
        my_paginator = Paginator(qs_goods, page_size)
        # 总个数
        count = my_paginator.count
        # 总页数
        num_pages = my_paginator.num_pages
        # 获取当前页对象
        try:
            my_page = my_paginator.page(page_now)
        except Exception as ex:
            if page_now > num_pages:
                page_now = num_pages
            elif page_now - 1 > 0:
                page_now = page_now - 1
            return redirect('/buyer/list/?page_now={}&sort={}'.format(page_now, sort))
        # 当页的商品集合
        list_goods = my_page.object_list
        # 是否有上一页
        has_previous = my_page.has_previous()
        # 是否有下一页
        has_next = my_page.has_next()
        # 获取分页页码：仿百度分页页码
        my_page_range = baidu_page(page_now, page_size, num_pages)
        # 6、查询商品同类型下的最新上架的2个商品
        list_new_goods = Goods.objects.filter(goodstype_id=goodstype_id).order_by('-id')[:2]
        ##################################准备数据字典####################################
        data = {
            'list_goods': list_goods,
            'num_pages': num_pages,
            'page_now': page_now,
            'page_size': page_size,
            'count': my_paginator.count,
            'my_page_range': my_page_range,
            'has_next': has_next,
            'has_previous': has_previous,
            'goodstype': goodstype,
            'list_new_goods': list_new_goods,
            'sort': sort,
        }
        ##################################响应####################################
        return render(request, 'buyer/list.html', data)


class SearchView(View):
    """列表页"""

    def get(self, request):
        ###################################获取参数###################################
        # 排序方式
        sort = request.GET.get('sort')
        # 搜索关键词
        key_word = request.GET.get('key_word')
        # 页码
        page_now = request.GET.get('page_now')
        ###################################判断排序方式###################################
        if not sort:
            sort = '0'
        ##################################判断处理页码####################################
        if not page_now:
            page_now = 1
        page_now = int(page_now)
        ##################################判断搜索关键词####################################
        if not key_word:
            key_word = ''
        ##################################根据排序方式获取结果集####################################
        # 判断排序方式，根据不同的排序方式获取对应的用于分页的结果集 '0': 按照id倒叙  '1': 按照价格  '2': 按照销量人气
        if sort == '1':
            qs_goods = Goods.objects.filter(name__icontains=key_word).order_by('price')
        elif sort == '2':
            qs_goods = Goods.objects.filter(name__icontains=key_word).order_by('-sale')
        else:
            qs_goods = Goods.objects.filter(name__icontains=key_word).order_by('id')
        ##################################分页相关####################################
        # 设置每页显示的数据的数量
        page_size = 10
        # 创建分页对象
        my_paginator = Paginator(qs_goods, page_size)
        # 总个数
        count = my_paginator.count
        # 总页数
        num_pages = my_paginator.num_pages
        # 获取当前页对象
        try:
            my_page = my_paginator.page(page_now)
        except Exception as ex:
            if page_now > num_pages:
                page_now = num_pages
            elif page_now - 1 > 0:
                page_now = page_now - 1
            return redirect('/buyer/list/?page_now={}&sort={}'.format(page_now, sort))
        # 当页的商品集合
        list_goods = my_page.object_list
        # 是否有上一页
        has_previous = my_page.has_previous()
        # 是否有下一页
        has_next = my_page.has_next()
        # 获取分页页码：仿百度分页页码
        my_page_range = baidu_page(page_now, page_size, num_pages)
        # 6、查询最新上架的2个商品
        list_new_goods = Goods.objects.order_by('-id')[:2]
        ##################################准备数据字典####################################
        data = {
            'list_goods': list_goods,
            'num_pages': num_pages,
            'page_now': page_now,
            'page_size': page_size,
            'count': my_paginator.count,
            'my_page_range': my_page_range,
            'has_next': has_next,
            'has_previous': has_previous,
            'list_new_goods': list_new_goods,
            'sort': sort,
            'key_word': key_word,
        }
        ##################################响应####################################
        return render(request, 'buyer/search.html', data)
