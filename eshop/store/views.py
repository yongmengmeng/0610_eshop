from django.shortcuts import render
from django.views import View
from store.models import *
from django.http import HttpResponse, JsonResponse
from store.util import *
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.paginator import Paginator
import uuid
import hashlib
import os


class RegisterView(View):
    """注册"""

    def get(self, request):
        return render(request, 'store/register.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        seller = Seller()
        seller.username = username
        seller.password = set_password(password)
        seller.save()
        return redirect('/store/login/')


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
            return redirect('/store/')
        else:
            # 响应
            return HttpResponse('登录失败')


# class BaseView(View):
#     """模板页"""
#
#     def get(self, request):
#         return render(request, 'store/base.html')


class IndexView(View):
    """首页"""

    @method_decorator(wrapper_login)
    def get(self, request):
        # 获取session中存储的用户id
        seller_id = request.session.get('logined')
        # 查询
        flag = Store.objects.filter(seller_id=seller_id).exists()
        # 数据
        data = {'flag': flag}
        # 渲染
        return render(request, 'store/index.html', data)


class AddStoreView(View):
    """添加店铺"""

    @method_decorator(wrapper_login)
    def get(self, request):
        # 获取所有商品类型
        list_storetype = StoreType.objects.order_by('id')
        return render(request, 'store/add_store.html', {'list_storetype': list_storetype})

    @method_decorator(wrapper_login)
    def post(self, request):
        # 获取参数
        name = request.POST.get("name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        money = request.POST.get("money")
        storetype_ids = request.POST.getlist("storetype_ids")
        descripton = request.POST.get("descripton")
        # 从session获取seller_id
        seller_id = request.session.get('logined')
        # 获取上传的文件对象
        image = request.FILES.get('image')
        # 新增并返回对象
        store = Store.objects.create(
            name=name,
            address=address,
            phone=phone,
            money=money,
            descripton=descripton,
            seller_id=seller_id,
            image=image
        )
        # 修改店铺类型
        for storetype_id in storetype_ids:
            store.storetypes.add(StoreType.objects.get(pk=storetype_id))
        # 修改
        store.save()
        # 响应
        return redirect('/store/')


class EditStoreView(View):
    """编辑店铺"""

    @method_decorator(wrapper_login)
    def get(self, request):
        # 从session获取seller_id
        seller_id = request.session.get('logined')
        # 查询店铺
        store = Store.objects.filter(seller_id=seller_id).first()
        # 查询所有商品类型
        list_storetype = StoreType.objects.order_by('id')
        # 响应
        return render(request, 'store/edit_store.html', {'store': store, 'list_storetype': list_storetype})

    @method_decorator(wrapper_login)
    def post(self, request):
        # 获取参数
        id = request.POST.get("id")
        name = request.POST.get("name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        money = request.POST.get("money")
        storetype_ids = request.POST.getlist("storetype_ids")
        descripton = request.POST.get("descripton")
        # 从session获取seller_id
        seller_id = request.session.get('logined')
        # 获取上传的文件对象
        image = request.FILES.get('image')
        # 查询对象
        store = Store.objects.filter(pk=id).first()
        # 修改属性-基本属性
        store.name = name
        store.address = address
        store.phone = phone
        store.money = money
        store.descripton = descripton
        store.money = money
        # 修改属性-logo图
        if image:
            # 删除原来的图片
            os.remove(os.path.join(settings.MEDIA_ROOT, store.image.name))
            # 修改为新图片对象
            store.image = image
        # 修改属性-店铺类型
        store.storetypes.clear()
        for storetype_id in storetype_ids:
            store.storetypes.add(StoreType.objects.get(pk=storetype_id))
        # 修改
        store.save()
        # 响应
        return redirect('/store/')


class AddGoodsView(View):
    """新增商品"""

    @method_decorator(wrapper_login)
    def get(self, request):
        # # 从session获取seller_id
        # seller_id = request.session.get('logined')
        # # 查询店铺
        # store = Store.objects.filter(seller_id=seller_id).first()
        # 查询所有商品类型
        list_goodstype = GoodsType.objects.order_by('id')
        # 响应
        return render(request, 'store/add_goods.html', {'list_goodstype': list_goodstype})

    @method_decorator(wrapper_login)
    def post(self, request):
        # 获取参数
        name = request.POST.get("name")
        price = request.POST.get("price")
        number = request.POST.get("number")
        productdate = request.POST.get("productdate")
        shelflife = request.POST.get("shelflife")
        goodstype_id = request.POST.get("goodstype_id")
        description = request.POST.get("description")
        # 从session获取seller_id
        seller_id = request.session.get('logined')
        # 查询店铺
        store = Store.objects.filter(seller_id=seller_id).first()
        # 获取上传的文件对象
        image = request.FILES.get('image')
        # 新增
        Goods.objects.create(
            name=name,
            price=price,
            number=number,
            productdate=productdate,
            shelflife=shelflife,
            goodstype_id=goodstype_id,
            description=description,
            store=store,
            image=image
        )
        # 响应
        return redirect('/store/')


class ListGoodsView(View):
    """商品列表"""

    @method_decorator(wrapper_login)
    def get(self, request):
        # 设置每页显示的数据的数量
        page_size = 10
        # 获取参数
        goods_name = request.GET.get('goods_name')
        page_now = request.GET.get('page_now')
        print('*' * 100)
        # 判断
        if not page_now:
            page_now = 1
        # 字符串转数字
        page_now = int(page_now)
        if not goods_name:
            goods_name = ''
        # 查询所有商品
        qs_goods = Goods.objects.filter(name__contains=goods_name).order_by('id')
        # 创建分页对象
        my_paginator = Paginator(qs_goods, page_size)
        # 获取当前页对象
        try:
            my_page = my_paginator.page(page_now)
        except:
            return redirect('/store/list/goods/?page_now={}&goods_name={}'.format(1, goods_name))

        # 总个数
        count = my_paginator.count
        # 总页数
        num_pages = my_paginator.num_pages
        # 开始数字
        num_from = (page_now - 1) * page_size + 1
        # 结束数字
        num_to = page_now * page_size
        if num_to > count:
            num_to = count
        # 当页的商品集合
        list_goods = my_page.object_list
        # 增加属性编号
        for index, goods in enumerate(list_goods):
            goods.num = index + num_from

        # 是否有上一页
        has_previous = my_page.has_previous()
        # 是否有下一页
        has_next = my_page.has_next()

        """页码处理,仿百度"""
        # 算法逻辑
        if page_now <= page_size / 2 + 1:
            page_start = 1
            page_end = page_size
        elif page_now > page_size / 2 + 1:
            page_start = page_now - page_size / 2
            page_end = page_now + page_size / 2 - 1
        # 对page_end进行校验，并重新赋值
        if page_end > num_pages:
            page_end = num_pages
        # 当不足page_num数目时，要全部显示，所以page_start要置为1
        if page_end <= page_size:
            page_start = 1
        # 处理得到分页页码列表
        page_start = int(page_start)
        page_end = int(page_end)
        my_page_range = [i for i in range(page_start, page_end + 1)]

        data = {
            'list_goods': list_goods,
            'num_pages': num_pages,
            'page_now': page_now,
            'page_size': page_size,
            'count': my_paginator.count,
            'num_from': num_from,
            'num_to': num_to,
            'my_page_range': my_page_range,
            'goods_name': goods_name,
            'has_next': has_next,
            'has_previous': has_previous,
        }
        # 响应
        return render(request, 'store/list_goods.html', data)

        # 1   1 - 10
        # 2   11 - 20
        # 3   21 - 30


class DeleteGoodsView(View):
    """商品列表"""

    @method_decorator(wrapper_login)
    def get(self, request):
        # 获取参数
        goods_name = request.GET.get('goods_name')
        page_now = request.GET.get('page_now')
        goods_id = request.GET.get('id')
        # 判断
        if not page_now:
            page_now = 1
        if not goods_name:
            goods_name = ''

        # 根据id查询对象
        goods = Goods.objects.filter(pk=goods_id).first()
        # 删除
        goods.delete()
        # 重定向
        return redirect('/store/list/goods/?page_now={}&goods_name={}'.format(page_now, goods_name))


class UpdateGoodsUpView(View):
    """修改商品上下架"""

    @method_decorator(wrapper_login)
    def get(self, request):
        # 获取参数
        goods_name = request.GET.get('goods_name')
        page_now = request.GET.get('page_now')
        up = request.GET.get('up')
        goods_id = request.GET.get('id')
        # 判断
        if not page_now:
            page_now = 1
        if not goods_name:
            goods_name = ''
        # 根据id查询对象
        goods = Goods.objects.filter(pk=goods_id).first()
        print('-' * 100)
        print(type(up), up)
        if up == '1':
            goods.up = 0
        else:
            goods.up = 1
        goods.save()
        # 重定向
        return redirect('/store/list/goods/?page_now={}&goods_name={}'.format(page_now, goods_name))
