import requests
import unittest
from models.Read_xls import readExcel
from myloging import Loging
import ddt
from read_writeyaml import MyYaml
from models import HTMLTestRunner3
from configpath import getpath
from models.myunit import mytest
import os
log = Loging()
report1 = os.path.join(getpath(), 'result', 'report.html')


@ddt.ddt
class TestGetNodeList_auth(unittest.TestCase):
    data = readExcel().get_xls('case_xy_huawei.xlsx', 'GetNodeList')

    @ddt.data(*data)
    def test_auth_GetNodeList(self, data):
        r = requests.post(MyYaml().config('url') + data.url, data.datas)
        self.result = r.json()
        time1 = r.elapsed.total_seconds()
        print('接口响应时间:' + str(time1))
        log.info('第{}条用例执行'.format(data.id))
        log.info('用例名称:{}'.format(data.name))
        log.info('接口响应时间为：{}'.format(time1))
        print(self.result)
        self.assertEqual(eval(data.expected)['status'], self.result['status'])

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestGetNodeList_auth))  #把写的用例加进来（将TestCalc类）加进来
f = open(report1,'wb')  #以二进制模式打开一个文件
runner = HTMLTestRunner3.HTMLTestRunner(f, title='unittest用例标题', description='这是用例描述')
runner.run(suite)  #运行用例（用例集合)




