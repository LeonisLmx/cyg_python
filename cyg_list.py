import time

import requests
from bs4 import BeautifulSoup
import random
import datetime
import cyg_business as cyg

url = 'http://tl.cyg.changyou.com/goods/selling?page_num={}&order_by=remaintime'
headers = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 "
    "Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 "
    "Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 "
    "Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 "
    "Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]
a = 1


def list(num):
    print("start task ,current num is %s" % num)
    try:
        scrotal = requests.get(url.format(num), headers={"User-Agent": random.choice(headers)})
        soup = BeautifulSoup(scrotal.content, "html.parser")
        # 在售账号
        result = soup.find_all('dl', {'item-info'})
        for entity in result:
            hourTime = entity.find('span', class_='less-than-day')
            dayTime = entity.find('p', class_='time')
            htmlTime = str(dayTime.string) if hourTime is None else str(hourTime.string)
            d1 = datetime.datetime.now()
            if '天' in htmlTime:
                htmlTime = htmlTime.lstrip("剩余时间：")
                d2 = d1 + datetime.timedelta(days=float(htmlTime[0:htmlTime.index('天')]),
                                             hours=float(htmlTime[htmlTime.index('天') + 1:htmlTime.index('小时')]),
                                             minutes=float(htmlTime[htmlTime.index('小时') + 2:htmlTime.index('分钟')]))
            else:
                d2 = d1 + datetime.timedelta(hours=float(htmlTime[0:htmlTime.index('小时')]),
                                             minutes=float(htmlTime[htmlTime.index('小时') + 2:htmlTime.index('分钟')]),
                                             seconds=float(htmlTime[htmlTime.index('分钟') + 2:htmlTime.index('秒')]))
            print('start to deal goods')
            cyg.good(str(entity.find('a')["href"]), d2.replace(microsecond=0), 1, None)  # 最近成交
    except Exception as e:
        print("list被限流，异常如下 %s" % e)
        print("因为异常，所以先sleep 1 秒")
        time.sleep(1)
        list(num)
    num = num + 1
    list(num)

if __name__ == '__main__':
    list(a)
