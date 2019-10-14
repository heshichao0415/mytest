import requests
import unittest
from models.myunit import mytest
from read_writeyaml import MyYaml

class GetRouteList_XY(mytest):
    """获取游戏路由表接口"""

    def test_auth_GetRouteList(self):
        """获取游戏路由表"""
        r = requests.post(self.url, self.data[1], timeout=MyYaml().config('timeout'), stream=True)
        self.result = r.json()
        time1 = r.elapsed.total_seconds()
        self.data[-1] = time1

if __name__ == '__main__':
    unittest.main()