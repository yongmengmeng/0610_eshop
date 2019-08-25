from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Seller(models.Model):
    username = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    nickname = models.CharField(max_length=32, verbose_name='昵称', null=True, blank=True)
    phone = models.CharField(max_length=11, verbose_name='电话', null=True, blank=True)
    email = models.EmailField(verbose_name='邮箱', null=True, blank=True)
    image = models.ImageField(upload_to='img', verbose_name='用户头像', null=True, blank=True)
    address = models.CharField(max_length=32, verbose_name='地址', null=True, blank=True)
    cardid = models.CharField(max_length=18, verbose_name='身份证', null=True, blank=True)

    class Meta:
        verbose_name='卖家'
        verbose_name_plural='卖家'
        db_table='eshop_seller'


class StoreType(models.Model):
    name = models.CharField(max_length=32, verbose_name='名称')
    descripton = models.TextField(verbose_name='描述')
    class Meta:
        verbose_name='店铺类型'
        verbose_name_plural='店铺类型'
        db_table='eshop_storetype'


class Store(models.Model):
    name = models.CharField(max_length=32, verbose_name='名称')
    address = models.CharField(max_length=32, verbose_name='地址')
    # descripton = models.TextField(verbose_name='描述')
    descripton = RichTextUploadingField(verbose_name='描述')
    image = models.ImageField(upload_to='img', verbose_name='logo图')
    phone = models.CharField(max_length=11, verbose_name='电话')
    money = models.FloatField(verbose_name='注册资金')
    seller = models.OneToOneField(to=Seller,on_delete=models.CASCADE,verbose_name='所属卖家')
    storetypes = models.ManyToManyField(to=StoreType, verbose_name='所属类型')

    class Meta:
        verbose_name = '店铺'
        verbose_name_plural = '店铺'
        db_table = 'eshop_store'

class Goods(models.Model):
    name = models.CharField(max_length=32, verbose_name='名称')
    price = models.FloatField(verbose_name='价格')
    image = models.ImageField(upload_to='img', verbose_name='图片')
    number = models.IntegerField(verbose_name='库存')
    description = models.TextField(verbose_name='描述')
    productdate = models.DateField(verbose_name='生产日期')
    shelflife = models.IntegerField(verbose_name='保质期')
    stores = models.ManyToManyField(to=Store, verbose_name='所属店铺')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'
        db_table = 'eshop_goods'

class GoodsImg(models.Model):
    image = models.ImageField(upload_to='img', verbose_name='地址')
    description = models.TextField(max_length=32, verbose_name='描述')
    goods = models.ForeignKey(to=Goods, on_delete=models.CASCADE, verbose_name='所属商品')

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = '商品图片'
        db_table = 'eshop_goodsimg'