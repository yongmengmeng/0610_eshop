from django.test import TestCase
import pymysql


def test1():
    my_connect = pymysql.connect(host='10.10.9.197', user='root', password='root', database='eshop', port=3306,
                                 charset='utf8')
    my_cursor = my_connect.cursor()
    for i in range(1000):
        sql = 'INSERT INTO eshop_goods(name) values({})'.format(i)
        my_cursor.execute(sql)
    my_connect.commit()
    my_cursor.close()
    my_connect.close()


def test2():
    my_connect = pymysql.connect(host='10.10.9.197', user='root', password='root', database='eshop', port=3306,
                                 charset='utf8')
    my_cursor = my_connect.cursor()
    sql = 'DELETE FROM eshop_goods'
    my_cursor.execute(sql)
    my_connect.commit()
    my_cursor.close()
    my_connect.close()


if __name__ == '__main__':
    # test2()
    test1()

