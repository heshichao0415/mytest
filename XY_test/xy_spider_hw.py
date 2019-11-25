import IPy
from myloging import Loging
import requests
import random
import json
from models.Read_xls import readExcel
log = Loging()
from configpath import getpath
import os
import datetime
import threading
import numpy
import time
path = getpath()
pa = os.path.join(path, 'XY_test', 'file.txt')

data = readExcel().get_xls('case_xy_huawei.xlsx', 'Sheet4')
data1 = readExcel().get_xls('case_xy_huawei.xlsx', 'Sheet5')

class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, number, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.number = number
        self.name = name

    def run(self):
        log.info('开启线程:{}'.format(self.name),)
        HW_test().test_hw(self.number)
        log.info('{}线程结束！'.format(self.name))

class HW_test():
    def __init__(self):
        self.data = data
        self.data1 = data1
        self.num1 = 0
        self.num = 0

    def test_data(self):
        self.cls = []         #原始
        self.cls1 = []        #最终
        self.cls2 = []         #分组
        for i in self.data:
            x = i[1]
            self.cls.append(x)
        for i in self.data1:
            x = i[1]
            self.cls1.append(x)
        list = numpy.array_split(self.cls, 3)
        for i in list:
            self.cls2.append(i)
        return self.cls, self.cls1, self.cls2

    def test_hw(self, n):
        # start_time = datetime.datetime.now()
        self.n = n
        cls3 = []
        sum = 0
        sum1 = 0
        self.test_data()
        for x in self.cls2[self.n]:
            log.info('正在执行线程Thread-{}'.format(self.n))
        # for x in self.cls:
            y = 0
            for i in self.cls1:
                a = IPy.IP(x) in IPy.IP(i)
                cls3.append(a)
                y += 1
            if len(self.cls1) == y:
                if True in cls3:
                    sum += 1
                    log.debug('判断成功%s' % x)
                else:
                    sum1 += 1
                    log.error('判断失败')
                del cls3[0:]
        log.info('成功数为：%s，失败数为：%s' % (sum, sum1))
        # end_time = datetime.datetime.now()
        # seconds = (end_time - start_time).seconds
        # start = start_time.strftime("%Y-%m-%d %H:%M:%S")
        # end = end_time.strftime("%Y-%m-%d %H:%M:%S")
        # minutes = seconds // 60
        # second = seconds % 60
        # run_time = str(minutes) + '分钟' + str(second) + '秒'
        # log.info('程序开始时间为：%s，结束时间为：%s，运行时间为%s' % (start, end, run_time))
# if __name__ == '__main__':
#     HW_test().test_hw()

#创建线程
thread = []
for i in range(0, 3):
    t = myThread(i, i, "Thread-{}".format(i))
    thread.append(t)

#开启线程
start_time = datetime.datetime.now()
for i in thread:
    i.start()
for i in thread:
    i.join()
end_time = datetime.datetime.now()
seconds = (end_time - start_time).seconds
start = start_time.strftime("%Y-%m-%d %H:%M:%S")
end = end_time.strftime("%Y-%m-%d %H:%M:%S")
minutes = seconds // 60
second = seconds % 60
run_time = str(minutes) + '分钟' + str(second) + '秒'
log.info('程序开始时间为：%s，结束时间为：%s，运行时间为%s' % (start, end, run_time))
