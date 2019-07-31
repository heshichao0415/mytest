import requests
import unittest
from models.myunit import mytest
from read_writeyaml import MyYaml
from write_readini import write_ini
from myloging import Loging

class ZYAccessToken_auth(mytest):
    """获取access_token"""

    def test_auth_ZYAccessToken(self):
        """access_token"""
        r = requests.post(self.url, self.data[1], timeout=MyYaml().config('timeout'), stream=True)
        self.result = r.json()
        #access_token写入ini文件
        try:
            write_ini(node='session', child='access_token', content=self.result['data']['access_token'])
            Loging().info('access_token写入成功')
        except Exception:
            Loging().error('access_token写入失败')

        time1 = r.elapsed.total_seconds()      #total_seconds 总时长，单位秒、、 获取接口响应时间
        self.data[-1] = time1

if __name__ == '__main__':
    unittest.main()