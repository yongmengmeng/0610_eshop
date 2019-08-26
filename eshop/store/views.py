from django.shortcuts import render
from django.views import View
from store.models import *
from django.http import HttpResponse, JsonResponse
from store.util import *
from django.utils.decorators import method_decorator
from django.conf import settings
import uuid
import os
import hashlib


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
