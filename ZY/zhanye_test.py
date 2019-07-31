import requests

from write_readini import write_ini
from write_readini import read_ini
from read_writeyaml import MyYaml
from myloging import Loging

log = Loging()
class Push_log():
    def __init__(self):
        self.log_url = MyYaml().config('url')
        self.log_dress = MyYaml().config('dress')

    def Log_zhanye(self):
        self.logdress = self.log_url + self.log_dress

        payload = {
                    'account': '637A5A9B-13B6-0C9A-D878-A33FE2D988CF',
                    'pass': 'yw2KMlSOXLABj9QZvmG3z8rVDWgunIdx'
             }
        r = requests.post(self.logdress, params=payload)
        result = r.json()
        #print(result['token'])
        #写入ini文件
        try:
            write_ini(node='session', child='token', content=result['token'])
            log.info('token写入成功')

        except:
            log.error('token写入失败')

        #读取ini文件
        try:
            read_token = read_ini(node='session', child='token')
            print(read_token)
            log.info('读取token成功')

        except:
            log.error('读取token失败')

if __name__ == '__main__':

    Push_log().Log_zhanye()