import requests
import unittest
from models.myunit import mytest
from read_writeyaml import MyYaml
import json
import ddt


class GetNodeList_XY(mytest):
    """获取节点列表接口"""


    def test_auth_GetNodeList(self):
        """获取游戏列表"""
        r = requests.post(self.url, json.dumps(self.data[1]), timeout=MyYaml().config('timeout'), stream=True)
        self.result = r.json()
        time1 = r.elapsed.total_seconds()
        self.data[-1] = time1


if __name__ == '__main__':
    unittest.main()