from myloging import Loging
import requests
log = Loging()
import unittest

url = 'http://118.123.165.10:9099/api/v1/xyhw/GetNodeList'
data = '{"userid":1650000000,"gameId":-536654,"isp2p":1,"fouter":1,"time":156897156,"sign":"8abb2f1c5f0b0271a38ed82c8472fc09"}'
class Getloadlist(unittest.TestCase):


    def test_test(self):
        r = requests.post(url, data)
        self.result = r.json()
        print(self.result)
        log.info('接口测试成功')

if __name__ == '__main__':
    unittest.main()