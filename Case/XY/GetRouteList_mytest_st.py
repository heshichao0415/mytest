import requests
from models.myunit import mytest
from myloging import Loging
from read_writeyaml import MyYaml
import ddt
from models.Read_xls import readExcel
logg = Loging()
import unittest
from models import HTMLTestRunner
from configpath import getpath
import os
report1 = os.path.join(getpath(), 'result', 'GetRouteList.html')

@ddt.ddt
class GetRouteList_auth(unittest.TestCase):
    """获取游戏路由表接口"""
    data = readExcel().get_xls('case_xy_huawei.xlsx', 'GetRouteList')

    @ddt.data(*data)
    def test_auth_GetRouteList(self, data):
        """获取游戏路由表"""
        r = requests.post(MyYaml().config('url') + data.url, data.datas, stream=True)
        self.result = r.json()
        time1 = r.elapsed.total_seconds()
        print('接口响应时间:' + str(time1))
        logg.info('第{}条用例执行'.format(data.id))
        logg.info('用例名称:{}'.format(data.name))
        logg.info('接口响应时间为：{}'.format(time1))
        print(self.result)
        self.assertEqual(eval(data.expected)['status'], self.result['status'], msg=self.result['msg'])

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(GetRouteList_auth))  #把写的用例加进来（将TestCalc类）加进来
f = open(report1,'wb')  #以二进制模式打开一个文件
runner = HTMLTestRunner.HTMLTestRunner(f, title='unittest用例标题', description='这是用例描述')
runner.run(suite)  #运行用例（用例集合)
