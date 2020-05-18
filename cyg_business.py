import random
import requests
from bs4 import BeautifulSoup
import re
import json
import pymysql
import schedule
import time

url = 'http://tl.cyg.changyou.com/goods/selling?page_num=1&order_by=remaintime'
goodsUrl = 'http://tl.cyg.changyou.com/goods/char_detail?serial_num=202004222244422422'
specialEquip = ["重楼戒", "真·重楼戒", "重楼玉", "真·重楼玉", "重楼链", "真·重楼链", "重楼甲", "真·重楼甲", "重楼肩", "真·重楼肩"]
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
conn = pymysql.connect("localhost", "root", "123456", "cyg")
# 得到一个可以执行SQL语句的光标对象
cursor = conn.cursor()

searchsql = "select * from goods where url = %(url)s"


def good(url, expireTime, status, dealTime):
    print('start good detail')
    searchinfo = {"url": url}
    print(url)
    if cursor.execute(searchsql, searchinfo) == 1:
        print("数据重复，直接跳过")
        return
    sql = "insert ignore into goods (name,sex,school,level,price,equip_score,mount,special_equip,skill_score," \
          "practice_score,gem_score,status,expire_time,url,max_hp,max_mp,server_info,deal_time) " \
          "values " \
          "(%(name)s,%(sex)s,%(menpai)s,%(level)s,%(price)s,%(equipScore)s,%(zuoqi)s,%(chonglou)s,%(xinfa)s," \
          "%(xiulian)s,%(gemXiuLian)s," \
          "%(status)s,%(time)s,%(url)s,%(maxHp)s,%(maxMp)s,%(qufu)s,%(dealTime)s);"

    goodsHtml = requests.get(url, headers={"User-Agent": random.choice(headers)})
    goodsSoup = BeautifulSoup(goodsHtml.content, 'html.parser')
    m = re.search(r"var\s+charObj\s+=\s+(.*);", str(goodsSoup))
    try:
        jd = json.loads(m.group(1))
    except:
        print(goodsHtml)
        print("限流超过")
        time.sleep(1)
        good(url, expireTime, status, dealTime)
        return
    chonglou = ""
    zuoqi = ""
    equip = jd["items"]["equip"]
    for i in equip:
        if str(equip[i]["name"]) in specialEquip:
            chonglou = chonglou + str(equip[i]["name"]) + "|"
        elif equip[i]["typeDesc"] == '坐骑':
            zuoqi = zuoqi + str(equip[i]["name"]).lstrip("坐骑：") + "|"
    info = {"name": jd["charName"],
            "sex": '女' if jd["sex"] == 0 else '男',
            "menpai": goodsSoup.find('span', class_='fn-other-menpai').string.lstrip("门派:"),
            "level": jd["level"],
            "price": goodsSoup.find('span', class_='ui-money-color').string.strip("￥"),
            "equipScore": jd["equipScore"],
            "zuoqi": zuoqi.rstrip("|"),
            "chonglou": chonglou.rstrip("|"),
            "xinfa": jd["xinFaScore"],
            "xiulian": jd["xiuLianScore"],
            "gemXiuLian": jd["gemXiuLianScore"],
            "status": status,
            "time": 0 if expireTime is None else expireTime,
            "url": url,
            "maxHp": jd["maxHp"],
            "maxMp": jd["maxMp"],
            "qufu": goodsSoup.find('p', class_='server-info J-message').text.lstrip("所在区服：").strip(),
            "dealTime": dealTime
            }
    print(info)
    print(cursor.execute(sql, info))
    cursor.connection.commit()


if __name__ == "__main__":
    schedule.every(10).seconds.do(list)
    while True:
        schedule.run_pending()
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()
