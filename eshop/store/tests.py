from django.test import TestCase
import pymysql
import random


def test1():
    # my_connect = pymysql.connect(host='10.10.9.197', user='root', password='root', database='eshop', port=3306,
    #                              charset='utf8')
    my_connect = pymysql.connect(host='10.10.2.102', user='root', password='root', database='my_eshop', port=3306,charset='utf8')
    my_cursor = my_connect.cursor()
    for i in range(1000):
        sql = 'INSERT INTO eshop_goods(name) values({})'.format(i)
        my_cursor.execute(sql)
    my_connect.commit()
    my_cursor.close()
    my_connect.close()


def test2():
    # my_connect = pymysql.connect(host='10.10.9.197', user='root', password='root', database='eshop', port=3306,charset='utf8')
    my_connect = pymysql.connect(host='10.10.2.102', user='root', password='root', database='my_eshop', port=3306,charset='utf8')
    my_cursor = my_connect.cursor()
    sql = 'DELETE FROM eshop_goods'
    my_cursor.execute(sql)
    my_connect.commit()
    my_cursor.close()
    my_connect.close()

def test3():
    # my_connect = pymysql.connect(host='10.10.9.197', user='root', password='root', database='eshop', port=3306,charset='utf8')
    my_connect = pymysql.connect(host='10.10.2.160', user='root', password='root', database='my_eshop', port=3306,charset='utf8')
    my_cursor = my_connect.cursor()

    sql = 'INSERT INTO eshop_goodstype(id,name,description,picture) values(%s,%s,%s,%s)'
    my_cursor.execute(sql,[1,'新鲜水果','新鲜水果','img/banner01.jpg'])
    my_cursor.execute(sql,[2,'海鲜水产','海鲜水产','img/banner02.jpg'])
    my_cursor.execute(sql,[3,'猪牛羊肉','猪牛羊肉','img/banner03.jpg'])
    my_cursor.execute(sql,[4,'禽类蛋品','禽类蛋品','img/banner04.jpg'])
    my_cursor.execute(sql,[5,'新鲜蔬菜','新鲜蔬菜','img/banner05.jpg'])
    my_cursor.execute(sql,[6,'速冻食品','速冻食品','img/banner06.jpg'])

    my_connect.commit()
    my_cursor.close()
    my_connect.close()
    print('OK')

def test4():
    # my_connect = pymysql.connect(host='10.10.9.197', user='root', password='root', database='eshop', port=3306,charset='utf8')
    my_connect = pymysql.connect(host='10.10.2.160', user='root', password='root', database='my_eshop', port=3306,charset='utf8')
    my_cursor = my_connect.cursor()

    for i in range(1,7):
        for j in range(100):
            sql = 'INSERT INTO eshop_goods' \
                  '(name,price,image,number,description,productdate,shelflife,store_id,goodstype_id,up,unite,sale) ' \
                  'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            my_cursor.execute(sql,[
                str(i)+str(j),random.randint(1,10000),'img/goods002.jpg',random.randint(1,10000),'好的很','2019-10-10',random.randint(1,10000),1,i,1,'500g',random.randint(1,10000)])
            my_connect.commit()
    my_cursor.close()
    my_connect.close()
    print('OK')


if __name__ == '__main__':
    # test1()
    # test2()
    # test3()
    test4()