from django.shortcuts import redirect, render
from store.models import *
import hashlib


def set_password(password):
    """md5加密"""
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    new_password = md5.hexdigest()
    return new_password


def wrapper_login(func):
    """登录验证的装饰器"""

    def inner(request, *args, **kwargs):
        logined = request.session.get('logined')
        if logined:
            return func(request, *args, **kwargs)
        else:
            response = redirect('/store/login/')

            # 获取请求路径
            redirct_url = request.get_full_path()
            # 保存到cookie
            response.set_cookie('redirct_url', redirct_url)

            return response

    return inner


def wrapper_store(func):
    """判断是否有店铺的装饰器"""

    def inner(request, *args, **kwargs):
        # 获取请求路径
        redirct_url = request.get_full_path()
        # 查询登录id
        logined = request.session.get('logined')
        # 查询店铺对象
        store = Store.objects.filter(seller_id=logined).first()
        # 判断是否有店铺
        if store:
            # 判断是否重复添加店铺
            if redirct_url == '/store/add/store/':
                return render(request, 'store/message.html', {'message': '您已经有一个店铺了，不能再添加了！！！'})
            else:
                return func(request, *args, **kwargs)
        else:
            if redirct_url == '/store/add/goods/':
                return render(request, 'store/message.html', {'message': '先添加店铺，再添加商品！！！'})
            elif redirct_url == '/store/edit/store/':
                return render(request, 'store/message.html', {'message': '目前没有店铺，请先添加店铺！！！'})
            else:
                return func(request, *args, **kwargs)

    return inner


"""
装饰器
1、没有到登录去登录（wrapper_login）
2、已经登录了，考虑店铺的问题（wrapper_store）
    1、如果店铺不存在，可以新增店铺
    2、如果店铺不存在，不能新增商品
    3、如果店铺不存在，不能编辑店铺
    4、如果店铺存在，不可以新增店铺


"""


def baidu_page(page_now, page_size, num_pages):
    """
    页码处理,仿百度
    :param page_now: 当前页码
    :param page_size: 每页显示的个数
    :param num_pages: 总页数
    :return: 分页的数字集合
    """
    # 处理数据
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
    # 处理得到分页页码列表,这是转int,因为python中除法运算结果是float,而range只能写int类型
    page_start = int(page_start)
    page_end = int(page_end)
    # 返回数字集合
    return range(page_start, page_end + 1)
