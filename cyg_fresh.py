# -*- coding: UTF-8 -*-

import datetime
import random

import requests
import schedule
from bs4 import BeautifulSoup

import cyg_detail as cyg

url = 'http://tl.cyg.changyou.com/goods/selling?page_num=1&order_by=remaintime'


def refresh():
    html = requests.get(url, headers={"User-Agent": random.choice(cyg.headers)})
    soup = BeautifulSoup(html.content, "html.parser")
    # pageNum = int(soup.find('a', class_="after").find_previous('span', class_='span').string)
    # cyg_list.list(pageNum)
    # print("pageNum is %s" % pageNum)
    try:
        list = soup.find('div', class_='list-new-good')
        for item in list.find_all('li'):
            if item.find('a') is not None:
                print(item.find('a').attrs['href'])
                stringTime = item.find('span', class_='col3').string
                print(stringTime)
                minute = 0
                print(stringTime)
                if stringTime != '刚刚':
                    minute = -int(stringTime.rstrip('分钟前'))
                now = datetime.datetime.now()
                publicityTime = now + datetime.timedelta(days=14, minutes=minute)
                cyg.good(item.find('a').attrs['href'], publicityTime.replace(microsecond=0), 0, None)
            print("-------")
    except Exception as e:
        print(e)
        # refresh()


if __name__ == '__main__':
    schedule.every(10).seconds.do(refresh)
    while True:
        schedule.run_pending()
