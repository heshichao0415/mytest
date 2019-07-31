import requests
import unittest
from models.myunit import mytest
from read_writeyaml import MyYaml

class QBfriend_auth(mytest):
    """接口数据推送"""

    def test_auth_QBfriend(self):
        """数据推送"""
        r = requests.get(self.url, self.data[1], timeout=MyYaml().config('timeout'), stream=True)
        self.result = r.json()

        time1 = r.elapsed.total_seconds()      #total_seconds 总时长，单位秒、、 获取接口响应时间
        self.data[-1] = time1

if __name__ == '__main__':
    unittest.main()