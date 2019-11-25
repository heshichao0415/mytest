import requests
import unittest
import ddt
from models.Read_xls import readExcel
from read_writeyaml import MyYaml
from myloging import Loging

log = Loging()

data = readExcel().get_xls('case_xy_huawei.xlsx', 'GetNodeList')
@ddt.ddt
class GetNodeList_XY(unittest.TestCase):
    """获取节点列表接口"""


    @ddt.data(*data)
    def test_auth_GetNodeList(self, data):
        """获取游戏列表"""
        r = requests.post(MyYaml().config('url') + data.url, data.datas, timeout=MyYaml().config('timeout'), stream=True)
        time1 = r.elapsed.total_seconds()
        self.result = r.json()
        try:
            self.assertEqual(self.result['status'], eval(data.expected)['status'], msg="预期结果与实际不符")
            if self.result['status'] == 0:
                # self.assertEqual(self.result['data'], (not None), msg='data为空')
                readExcel().write_xls('case_xy_huawei.xlsx', 'GetNodeList', int(data.id) + 1, str(self.result), 'pass')
                log.info('用例执行成功')
            else:
                log.error('用例执行失败')
                readExcel().write_xls('case_xy_huawei.xlsx', 'GetNodeList', int(data.id) + 1, str(self.result), 'faled')

        except:
            readExcel().write_xls('case_xy_huawei.xlsx', 'GetNodeList', int(data.id), str(self.result), 'faled')
            log.error('用例支持失败，回写成功')
        print(time1)


if __name__ == '__main__':
    GetNodeList_XY().test_auth_GetNodeList()