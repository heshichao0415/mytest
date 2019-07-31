import requests
import unittest
from models.myunit import mytest
from read_writeyaml import MyYaml
from write_readini import write_ini
from myloging import Loging
log = Loging()


class QBInterface_auth(mytest):
    """获取access_token"""

    def test_login_token(self):
        """接口账号登录"""

        r = requests.post(self.url, data=self.data[1], timeout=MyYaml().config('timeout'), stream=True)
        self.result = r.json()

        time1 = r.elapsed.total_seconds()      #total_seconds 总时长，单位秒、、 获取接口响应时间
        self.data[-1] = time1
        # 写入ini文件
        try:
            write_ini(node='session', child='token', content=self.result['token'])
            log.info('token写入成功')

        except:
            log.error('token写入失败')

if __name__ == '__main__':
    unittest.main()
