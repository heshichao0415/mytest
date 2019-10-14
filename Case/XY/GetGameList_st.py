import requests
import unittest
from models.myunit import mytest
from read_writeyaml import MyYaml
case_name = 5
class GetGameList_XY(mytest):
    """获取游戏列表接口"""

    def test_auth_GetGameList(self):
        """获取游戏列表"""
        if case_name == 5:
            self.data[1]['openID1'] = 'dsgdsgsdg'           #需要改变的参数
            r = requests.post(self.url, self.data[1], timeout=MyYaml().config('timeout'), stream=True)
            self.result = r.json()
            time1 = r.elapsed.total_seconds()
            self.data[-1] = time1

if __name__ == '__main__':
    unittest.main()


