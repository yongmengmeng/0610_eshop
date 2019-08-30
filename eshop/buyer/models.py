from django.db import models
from db.basemodel import BaseModel
from django.contrib.auth.models import AbstractUser


class Buyer(AbstractUser,BaseModel):
    phone = models.CharField(max_length=11, verbose_name='电话', null=True)
    addr = models.CharField(max_length=32, verbose_name='联系地址', null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '买家'
        verbose_name_plural = '买家'
        db_table = 'eshop_buyer'


class Address(BaseModel):
    name = models.CharField(max_length=32, verbose_name='收货人姓名')
    phone = models.CharField(max_length=32, verbose_name='收货人电话')
    addr = models.CharField(max_length=32,verbose_name='收货地址')
    postcode = models.CharField(max_length=32, verbose_name='收货地址邮编')
    buyer = models.ForeignKey(to=Buyer, on_delete=models.CASCADE, verbose_name='所属用户')
    isdefault = models.BooleanField(default=False, verbose_name='是默认地址')

    def __str__(self):
        return self.addr

    class Meta:
        verbose_name = '收货地址'
        verbose_name_plural = '收货地址'
        db_table = 'eshop_address'