import requests
import unittest
from models.myunit import mytest
from read_writeyaml import MyYaml


class Login_XY(mytest):
    """用户登录授权"""

    def test_auth_Login(self):
        """登录"""

        r = requests.post(self.url, data=self.data[1], timeout=MyYaml().config('timeout'), stream=True)
        self.result = r.json()
        time1 = r.elapsed.total_seconds()
        self.data[-1] = time1

if __name__ == '__main__':
    unittest.main()
