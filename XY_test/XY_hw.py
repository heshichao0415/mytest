import IPy
from myloging import Loging
import requests
import random
import json

log = Loging()

class XY_hw():
    def __init__(self):
        self.url = 'http://api-ip-bgp-yw.wyjsq.com:33316/asn/routing_table'
        self.url1 = 'http://api-ip-bgp-yw.wyjsq.com:33316/asn/routing_table/src/'

    def test_get_data(self):
        r = requests.get(url=self.url)               #合并后的网段接口请求
        result = r.json()
        data = result['data']['routing_table']
        self.asn = result['data']['asn']
        return data

    def test_get_data1(self):                         #原始网段接口请求
        self.url1 = self.url1 + str(self.asn)
        r = requests.get(url=self.url1)
        result = r.text
        return result

    def test_hw(self):
        sum = 0           #合并后的网段IP个数
        sum2 = 0          #包含的原始网段个数
        sum3 = 0          #不包含的原始网段个数
        cls3 = []         #包含的网段
        cls4 = []         #没有包含的网段
        cls1 = []         #原始网段
        cls = []          #返回的网段ip列表总数
        list = self.test_get_data()          #接口返回的合并网段
        list2 = self.test_get_data1()        #接口返回的原始网段
        a = json.dumps(list2)
        # e = a[1:-2].split("\\n")
        b = a.replace('\\n', '","')
        c = eval(b)
        for i in c:
            cls1.append(i)
        #判断原始网段是否包含在合并网段中
        cls2 = []
        for i in cls1:
            c = 0
            for x in list:
                a = IPy.IP(i) in IPy.IP(x)
                cls2.append(a)
                c += 1
            if c == len(list):
                # print(cls2)
                if True in cls2:
                    cls3.append(i)
                    sum2 += 1
                    log.info('原始网段%s包含在合并网段中' % i)
                else:
                    cls4.append(i)
                    sum3 += 1
                    log.info('原始网段%s没有包含在在合并网段中' % i)
            del cls2[0:]

        log.info('原始网段个数为：%s，合并后的网段个数为：%s，原始网段包含在合并网段中的个数：%s，'
                 '原始网段没有包含在合并网段中的个数为：%s，包含的原始网段为：%s，'
                 '不包含的原始网段为：%s' % (len(cls1), len(list), sum2, sum3, cls3, cls4))

        print('===============')
        print('原始网段为：%s' % list)
        print('合并后的网段为:%s' % cls1)
        print('===============')
        #网段包含的所有的IP
        for i in list:
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

if __name__ == "__main__":
    XY_hw().test_hw()


