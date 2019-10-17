import IPy
from myloging import Loging
import requests
import random
import json
from models.Read_xls import readExcel
log = Loging()

data = readExcel().get_xls('case_xy_huawei.xlsx', 'Sheet2')

class XY_hw():
    def __init__(self):
        self.url = 'http://api-ip-bgp-yw.wyjsq.com:33316/asn/routing_table'
        self.url1 = 'http://api-ip-bgp-yw.wyjsq.com:33316/asn/routing_table/src/'
        self.url2 = 'http://admin-ip-bgp-yw.wyjsq.com:33319/merge_network'
        self.data = data

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

    def test_post_data(self):
        sum1 = 0  # 成功的
        sum2 = 0  # 失败的
        failed = []    #失败的原网段

        for i in self.data:
            self.number = i[0]         #编号
            self.data1 = i[1]          #原始网段
            self.expected = i[2]       #预期结果
            self.data = {
                'ip_src': self.data1,
                'min_lose': 16,            #两组数据间缺失IP数 <= 允许最小缺失阀值， 默认16
                'max_lose': 256,           #允许最大缺失阀值，默认256
                'pct_lose': .4,            #已整合IP个数*阀值,默认.4
                'drop_mask': 32,           #设定丢弃阀值，默认28
                'pct_limit': .8,           #网段IP数*阀值， 默认.8
                'min_mask': 32             #最小网段阀值,默认32
            }
            r = requests.post(self.url2, self.data)
            self.result = r.json()
            actual = self.result['data'][0]
            expected = self.expected
            log.info('第%s条数据执行结果' % self.number)
            if actual == expected:
                sum1 += 1
                log.info('原始网段为:%s 预期结果：%s，接口返回的实际结果：%s，判断相同' % (self.data1, expected, actual))
            else:
                failed.append(self.data1)
                sum2 += 1
                log.error('原始网段为:%s 预期结果：%s，接口返回的实际结果：%s，判断不相同' % (self.data1, expected, actual))
            print(self.result)
        log.debug('成功数为：%s，失败数为：%s' % (sum1, sum2))
        log.error('失败的原始网段为：%s' % failed)

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
            'drop_mask': 32,           #设定丢弃阀值，默认28
            'pct_limit': .8,           #网段IP数*阀值， 默认.8
            'min_mask': 32             #最小网段阀值,默认32
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
    XY_hw().test_post_data()


