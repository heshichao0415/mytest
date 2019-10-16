import requests
import unittest
from models.Read_xls import readExcel
from myloging import Loging
import ddt
from read_writeyaml import MyYaml
import HTMLTestRunner
from configpath import getpath
import os

report1 = os.path.join(getpath(), 'result', 'sf.html')


@ddt.ddt
class TestGetNodeList_auth(unittest.TestCase):
    data = readExcel().get_xls('case_xy_huawei.xlsx', 'Sheet1')

    @ddt.data(*data)
    def test_auth_GetNodeList(self, data):
        r = requests.post(MyYaml().config('url') + data.url, data.datas)
        self.result = r.json()
        time1 = r.elapsed.total_seconds()
        print('接口响应时间:' + str(time1))
        Loging().debug('第{}条用例执行'.format(data.id))
        Loging().debug('用例名称:"{}"'.format(data.name))
        print(self.result)
        self.assertEqual(eval(data.expected)['status'], self.result['status'])

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGetNodeList_auth))
    fp = open(report1, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='output_result_title')
    # runner = unittest.TextTestRunner()
    runner.run(suite)



