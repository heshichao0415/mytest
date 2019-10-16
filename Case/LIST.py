#列表排序
# a = [-4,5,2,9,6,20,-10]    #列表
# a.sort(reverse=True)      #列表降序排列  reverse=True代表降序
# print(a)
# a.sort(reverse=False)     #列表升序排列  reverse=False代表升序
# print(a)

#
# a = '1,2,3,4,5'
# c = list(eval(a))
# print(c)

# a = (1,2,3,4,5)
# b = {'a':'5', 'c':'7'}
#
# if isinstance(a, tuple):
#     print('OK')
# else:
#     print('NO')
# import redis
#
# poll = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True, db=0)
# r = redis.Redis(connection_pool=poll)
# # r.lpush('my',11,22,44)
# # # r.lpush('my1',0,22,44)
# # r.delete('my''my1')
# print(r.lrange('zhanye_dmp', 0, -1))
# # print(r.lrange('my1', 0, -1))
# # # r.delete('my')
#
# # a = ['adad', 'adad', 'awearf']
# # result = r.lpop('my')
# # print(result)
# r.delete('my')
# print(r.lrange('my',0 , -1))
# from models.myunit_per import ReadYaml
#
# all_test_fun = ReadYaml().case_info_data('QBfriend_auth')
# for case_ins in all_test_fun:
#     case_info = {'case_name': case_ins[1]['case_name'], 'mode': case_ins[1]['mode'],
#                  'api_url': case_ins[1]['url'],
#                  'time': 0, 'statues': '', 'info': ''}
# print(all_test_fun)
# print(case_info)
# import _thread
# import time
# def print_time(threadName, day):
#     count = 0
#     while count < 5:
#         time.sleep(day)
#         count += 1
#         print("%s, %s" % (threadName, time.ctime(time.time())))
#
# try:
#     """创建线程"""
#     print("开启线程")
#     _thread.start_new_thread(print_time, ("threadName-1", 2))
#
# except:
#     print("Error: unable to start thread")
# while 1:
#     pass
#正则表达式
import re
# a = "www.baidu.com"
# c = re.match('www', a,).span()
# print(c)
# text1 = 'Hi, I am Shirley Hilton. I am his wife.'
# text = "site sea sue sweet see case sse ssee loses"
# text2 = 'I am Shirley Hilton. I am his wife'
# text3 = 'i am phone is aa15882438601ddsjh, 13882438601'
# e = re.findall(r'\d[0-9]*\d', text3)
# print(e)
# d = re.findall(r'I.*?e', text2)
# print(d)
# c = re.findall(r"\bh\S*?s\b", text1)
# print(c)
# m = re.findall(r"\bs\S*?e\b", text)
# print(m)
# phone = "2004-959-559 # 这是一个电话号码"
# num = re.sub(r"#.*$", '', phone)  #删除注释
# num1 = re.sub(r"\D", '', phone)   #移除非数字内容
# print(num1)   #结果2004959559
# print(num)    #结果2004-959-559
# text = 'imma am phone is aa15882438601ddsjh, 13882438601'
# a = re.search('phone', text)
# print(a.span())
# str = 'fhsfklsngkbslg'
# print(str[1])
# print(str[0])
# print(str[7-10])

# list1 = []
# i = 0
# list = [2,9,8,6,3,10,40,27]
# for a in list:
#     if a%2 == 0:
#         list.remove(a)
#         print(list)
# import random
# a = '158{}'.format(random.randint(00000000, 99999999))
# b = random.randrange(1,101,2)
# print(b)
# c = []
# list = [1,2,3,4,5,6,7,8,9,10]
# for a in list:
#     if a % 2 == 0:
#         c.append(a)
# print(c)
# list.sort(reverse=True)
# print(list)
# import requests
# class Login():
#     def test_login(self, url, data):
#         r = requests.post(url=url, data=data, timeout=5)
#         self.result = r.json()
#         print(self.result)
#
# if __name__ == '__main__':
#     Login().test_login()
# a = '1,2,3,4,5'
# c = list(a)
# print(c)

# print(r'\b')
# print('\b')
# import random
# from myloging import Loging
# log = Loging()
# a = [1, 2, 3, 4]
# b = [[1,2],[2,5],[3,6],[7,8]]
# sum1 = 0
# sum2 = 0
# cls = []
# for i in a:
#     s = 0
#     for x in b:
#         c = i in x
#         cls.append(c)
#         s += 1
#         print(cls)
#     if s == 4:
#         if True in cls:
#             sum1 += 1
#             log.info('原始网段%s包含在合并网段中' % i)
#         else:
#             sum2 += 1
#             log.info('原始网段%s没有包含在在合并网段中' % i)
#     del cls[0:]
# print(cls)
# log.info('匹配成功的个数为：%s，匹配失败的个数为：%s，原始网段为：%s' % (sum1, sum2,a))
# print(cls)
#
# a = 'safasfasffa'
# c = random.choice(a)
# print(c)

from configpath import getpath
import os

path = getpath()

pa = os.path.join(path, 'result', 'file.html')

with open(pa, 'w') as e:
    e.write('afsfsfasg')