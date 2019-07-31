import requests
import unittest
from models.myunit import mytest
from read_writeyaml import MyYaml
from write_readini import read_ini

class ZYrecharge_auth(mytest):
    """充值接口"""
    def test_auth_ZYrecharge(self):
        """或者充值ID"""
        r = requests.get(self.url, self.data[1], headers=self.headers, timeout=MyYaml().config('timeout'), stream=True)
        self.result = r.json()

        time1 = r.elapsed.total_seconds()      #total_seconds 总时长，单位秒、、 获取接口响应时间
        self.data[-1] = time1

if __name__ == '__main__':
    unittest.main()