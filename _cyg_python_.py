import requests
import io
import sys
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,'utf-8')

ua_header = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}

r = requests.get('http://tl.cyg.changyou.com/',headers=ua_header)

r.encoding = 'utf-8'

result = r.text

bs = BeautifulSoup(result,'html.parser')

result = bs.find_all('dl',{'item-info'})

for entity in result:
    print(entity)
    print("链接地址：%s" % entity.find('a')["href"])
    print("门派 %s" % entity.find('span',{'name'}).text)
    print(entity.select('a'))
    print("名字 %s" % entity.find('span',{'name'}).text)
    print("是否拥有重楼 %s" % entity.find('i',{'icon-cl'})['title'])
    results = entity.find_all('span', {'di'})
    print("装备评分：%s" % results[0].find('b').text)
    print("修炼评分：%s" % results[1].find('b').text)
    print("进阶评分：%s" % results[2].find('b').text)
    print("----------------")