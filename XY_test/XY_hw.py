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

path = getpath()
pa = os.path.join(path, 'XY_test', 'file.txt')

data = readExcel().get_xls('case_xy_huawei.xlsx', 'Sheet3')

class XY_hw():
    def __init__(self):
        self.url = 'http://api-ip-bgp-yw.wyjsq.com:33316/asn/routing_table/1008611'                  #合并后的网段
        self.url1 = 'http://api-ip-bgp-yw.wyjsq.com:33316/asn/routing_table/src/1008611'            #原始网段
        self.url2 = 'http://admin-ip-bgp-yw.wyjsq.com:33319/merge_network'
        self.data = data

    def test_get_data(self):
        r = requests.get(url=self.url)               #合并后的网段接口请求
        result1 = r.text
        return result1

    def test_get_data1(self):                         #原始网段接口请求
        r = requests.get(url=self.url1)
        result = r.text
        with open(pa, 'w') as e:
            e.write(result)
        return result

    def test_post_data(self):
        sum1 = 0  # 成功的
        sum2 = 0  # 失败的
        failed = []    #失败的原网段
        list3 = []     #预期结果值
        for i in self.data:
            self.number = int(i[0])         #编号
            self.data1 = i[1]          #原始网段
            self.expected = i[2]       #预期结果
            self.dro_mask = int(i[3])  # 掩码阈值
            if self.number in (3, 6, 9, 12, 17, 18, 21, 24, 27, 30, 35, 36):
                a = json.dumps(self.expected)
                b = a.replace('\\n', '","')
                c = eval(b)
                for i in c:
                    list3.append(i)
            else:
                list3.append(self.expected)
            self.data = {
                'ip_src': self.data1,
                'min_lose': 16,            #两组数据间缺失IP数 <= 允许最小缺失阀值， 默认16
                'max_lose': 256,           #允许最大缺失阀值，默认256
                'pct_lose': .4,            #已整合IP个数*阀值,默认.4
                'drop_mask': 33,           #设定丢弃阀值，默认28
                'pct_limit': .8,           #网段IP数*阀值， 默认.8
                'min_mask': self.dro_mask             #掩码,默认32
            }
            r = requests.post(self.url2, self.data)
            self.result = r.json()
            actual = self.result['data']
            log.info('第%s条数据执行结果' % self.number)
            if actual == list3:
                sum1 += 1
                log.info('原始网段为:%s 预期结果：%s，接口返回的实际结果：%s，判断相同' % (self.data1, list3, actual))
            else:
                failed.append(self.data1)
                sum2 += 1
                log.error('原始网段为:%s 预期结果：%s，接口返回的实际结果：%s，判断不相同' % (self.data1, list3, actual))
            del list3[0:]
        log.debug('成功用例数为：%s，失败用例数为：%s' % (sum1, sum2))
        log.error('失败的原始网段为：%s' % failed)

    def test_hw(self):
        start_time = datetime.datetime.now()
        sum = 0           #合并后的网段IP个数
        sum2 = 0          #包含的原始网段个数
        sum3 = 0          #不包含的原始网段个数
        cls3 = []         #包含的网段
        cls4 = []         #没有包含的网段
        cls1 = []         #原始网段
        cls5 = []         #合并后的网段
        cls6 = []         #需要丢弃的网段
        cls = []          #返回的网段ip列表总数
        list = self.test_get_data()          #接口返回的合并网段
        list2 = self.test_get_data1()        #接口返回的原始网段
        a = json.dumps(list2)
        # e = a[1:-2].split("\\n")           #转换为列表
        b = a.replace('\\n', '","')
        c = eval(b)
        for i in c:
            if int(i[-2:]) not in (28, 29, 30, 31, 32):
                cls1.append(i)
        x = json.dumps(list)
        y = x.replace('\\n', '","')
        z = eval(y)
        for i in z:
            if int(i[-2:]) != 31:
                cls5.append(i)
        if cls1 == cls5:
            log.info('不合并的原始数据与合并后的数据相同')
        else:
            log.error('不合并的原始数据与合并后的数据不相同')

        #判断原始网段是否包含在合并网段中
        cls2 = []
        for i in cls1:
            if int(i[-2:]) in (28, 29, 30, 31, 32):
                cls6.append(i)
            c = 0
            for x in cls5:
                if int(i[-2:]) not in (28, 29, 30, 31, 32):
                    a = IPy.IP(i) in IPy.IP(x)
                    cls2.append(a)
                    c += 1
            if c == len(cls5):
                if True in cls2:
                    cls3.append(i)
                    sum2 += 1
                    log.info('原始网段%s包含在合并网段中' % i)
                else:
                    cls4.append(i)
                    sum3 += 1
                    log.error('原始网段%s没有包含在在合并网段中' % i)
            del cls2[0:]
        end_time = datetime.datetime.now()
        seconds = (end_time - start_time).seconds          #second 忽略天 只看时分秒,,total_seconds() 真正的时间差 包含天
        start = start_time.strftime("%Y-%m-%d %H:%M:%S")
        end = end_time.strftime("%Y-%m-%d %H:%M:%S")
        minutes = seconds // 60
        second = seconds % 60
        run_time = str(minutes) + '分钟' + str(second) + '秒'
        log.info('原始网段个数为：%s，合并后的网段个数为：%s，原始网段包含在合并网段中的个数：%s，'
                 '原始网段没有包含在合并网段中的个数为：%s，丢弃的网段个数为：%s，不包含的原始网段为：%s'
                  % (len(cls1), len(cls5), sum2, sum3, len(cls6), cls4,))
        log.info('开始时间为：%s，结束时间为：%s，运行时间为：%s' % (start, end, run_time))
        print('===============')
        print('原始网段为：%s' % cls1)
        print('合并后的网段为：%s' % cls5)
        print('===============')
        # 判断不合并的原始网段和合并后的网段是否相同
        if cls5 == cls1:
            log.info('不合并的原始网段和合并后的网段相同')
        else:
            log.error('不合并的原始网段和合并后的网段不相同')
        log.info('原始网段个数为：%s，合并后的网段为：%s' % (len(cls1), len(cls5)))
        print('===============')
        print('原始网段为：%s' % cls1)
        print('合并后的网段为：%s' % cls5)
        print('===============')

        # 网段包含的所有的IP
        for i in cls5:
            if int(i[-2:]) == 24:      #需要舍弃的网段参数
                ip = IPy.IP(i)
                sum = sum + ip.len()
                for x in ip:
                    x = str(x)
                    if (x[-2:]) != '.0' and (x[-len((str(ip.len()))):]) != str(ip.len()-1):      #需要舍弃的无用IP
                        cls.append(x)
        sum1 = len(cls)                  #  舍弃后的IP个数
        #随机取出10个IP列表
        a = random.sample(cls, 10)
        a.append('192,168,1,21')
        for x in a:
            if x not in cls:
                print(x + '没有在接口返回的列表内')
        log.info('接口返回的网段个数为：%s, 共计IP个数为：%s，'
                 '舍弃无用的IP后总数为：%s，舍弃的无效IP个数为：%s' % (len(list), sum, sum1, (sum-sum1)))

    def test_post_data1(self):
        ip_src = """
        104.52.1.1-104.52.1.80
        104.52.1.100-104.52.1.230
        """
        self.data = {
            'ip_src': ip_src,
            'min_lose': 16,            #两组数据间缺失IP数 <= 允许最小缺失阀值， 默认16
            'max_lose': 256,           #允许最大缺失阀值，默认256
            'pct_lose': .4,            #已整合IP个数*阀值,默认.4
        }
        r = requests.post(self.url2, self.data)
        self.result = r.json()
        actual = self.result['data'][0]
        expected = '104.52.1.0/24'
        if actual == expected:
            log.info('原始网段为:%s 预期结果：%s，接口返回的实际结果：%s，判断相同' % (ip_src, expected, actual))
        else:
            log.info('原始网段为:%s 预期结果：%s，接口返回的实际结果：%s，判断不相同' % (ip_src, expected, actual))
        print(self.result)

if __name__ == "__main__":
    # XY_hw().test_post_data()
    # XY_hw().test_get_data1()
    XY_hw().test_hw()



