import requests
import sys
import json

# 新增
# 1 7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a226531306164633339343962613539616262653536653035376632306638383365222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d https://xxl-job-admin-benchmark.matrix.co

# 删除
# 2 7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a226531306164633339343962613539616262653536653035376632306638383365222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d https://xxl-job-test.matrix.co 1,2,3,4

# 第一个参数是 operate 操作，1是新增，2是删除
# 第二个参数是 cookie
# 第三个为http参数  分割不同的环境
# 第四个参数为业务参数  add 的时候可以不传，但是需要配置config.json文件

http = 'http://localhost:8080'
add_url = '/jobinfo/add'
list_url = '/jobinfo/pageList'
remove_url = '/jobinfo/remove'
start_url = '/jobinfo/start'

headers = {
    'cookie': 'Idea-d59e3cab=f4d27c34-ed8b-49d9-b6e5-818d4d17ef16; '
              'UM_distinctid=170384f8fcf5b8-079f5ac535dd41-1d316653-1aeaa0-170384f8fd0993; '
              'CNZZDATA1260945749=1939353350-1581489601-%7C1582093008; '
              'XXL_JOB_LOGIN_IDENTITY'
              '=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a226531306164633339343962613539616262653536653035376632306638383365222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d '
}

add_list = [{
    'jobGroup': 2,
    'jobDesc': 'test1',
    'cronGen_display': '0 * 3 * * ?',
    'jobCron': '0 * 3 * * ?',
    'executorHandler': 'testBtyPython',
    'author': 'aa'
}, {
    'jobGroup': 2,
    'jobDesc': 'test2',
    'cronGen_display': '0 * 4 * * ?',
    'jobCron': '0 * 4 * * ?',
    'executorHandler': 'testBtyPython2',
    'author': 'aa'
}]

data = {
    'jobGroup': 2,
    'jobDesc': 'depositAnalysis',
    'executorRouteStrategy': 'FIRST',
    'cronGen_display': '0 * 2 * * ?',
    'jobCron': '0 * 2 * * ?',
    'glueType': 'BEAN',
    'executorHandler': 'testBtyPython',
    'executorBlockStrategy': 'SERIAL_EXECUTION',
    'childJobId': '',
    'executorTimeout': 0,
    'executorFailRetryCount': 0,
    'author': 'aa',
    'alarmEmail': '',
    'executorParam': '',
    'glueRemark': 'GLUE代码初始化'
}

list_data = {
    'jobGroup': 2,
    'triggerStatus': -1
}

remove_list = [2, 3, 4, 5]


def add(item):
    r = requests.post(add_url, item, headers=headers)
    print(r.json())


def list():
    result = requests.post(list_url, list_data, headers=headers)
    print(result.json())
    return result.json()


def remove(data):
    r = requests.post(remove_url, data, headers=headers)
    print(r.json())


def start(item):
    r = requests.post(start_url, item, headers=headers)
    print(r.json())


if __name__ == '__main__':
    operate = sys.argv[1]
    cookie = sys.argv[2]
    http = sys.argv[3]
    list_url = http + list_url
    start_url = http + start_url
    with open("config.json", 'r', encoding='UTF-8') as f:
        add_list = json.load(f)
    print(add_list)
    if operate == '1':
        add_url = http + add_url
        print("start add")
        for item in add_list:
            print(item)
            data['jobGroup'] = item['jobGroup']
            data['jobDesc'] = item['jobDesc']
            data['cronGen_display'] = item['cronGen_display']
            data['jobCron'] = item['jobCron']
            data['executorHandler'] = item['executorHandler']
            data['author'] = item['author']
            add(data)
        lists = list()
        for entity in lists['data']:
            startData = {'id': int(entity['id'])}
            start(startData)
    elif operate == '2':
        remove_url = http + remove_url
        list_params = sys.argv[4]
        remove_list = list_params.split(",")
        print("start remove")
        print(remove_list)
        for item in remove_list:
            print('item is %s and url is %s', (item, remove_url))
            data = {'id': int(item)}
            print(data)
            remove(data)
