# -*- coding: UTF-8 -*-

import datetime
import random

import requests
from bs4 import BeautifulSoup

import cyg_detail as cyg

url = 'http://tl.cyg.changyou.com/goods/selling?page_num=1&order_by=remaintime'


# 获取最近成交
def list():
    print("start task")
    scrotal = requests.get(url, headers={"User-Agent": random.choice(cyg.headers)})
    soup = BeautifulSoup(scrotal.content, "html.parser")
    for item in soup.select('.order-list li'):
        try:
            a = item.select('.good-name')[0]
            print('账号名称是：%s , 链接地址是：%s, 价格是：%s，成交时间是：%s' % (
                a.get_text(), a.attrs['href'], item.select('.good-price')[0].get_text(),
                item.select('.order-time')[0].get_text()))
            print(datetime.datetime.now().year)
            time = str(datetime.datetime.now().year) + "-" + item.select('.order-time')[0].string.rstrip("成交")
            cyg.good(str(a.attrs['href']), item.select('.order-time')[0].get_text(), 2, time)
            print(time)
        except Exception as e:
            print(e)
            print("error!")


if __name__ == '__main__':
    list()
