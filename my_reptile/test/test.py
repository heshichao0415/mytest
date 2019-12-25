import requests
from read_writeyaml import MyYaml
from bs4 import BeautifulSoup
from configpath import getpath
import os
import json

class Myreptile(object):

    def __init__(self):
        self.url = MyYaml().reptile('url')
        self.url2 = MyYaml().reptile("url2")
        self.path = os.path.join(getpath(), 'my_reptile', 'result', MyYaml().reptile('file'))
        self.re = MyYaml().reptile("matching")

    def test_reptile_get(self):
        str_html = requests.get(self.url)           #Get方式获取网页数据，此时只是一个对象
        # print(str_html.text)                        #打印网页源码
        soup = BeautifulSoup(str_html.text, "lxml")         #解析源码
        # print(soup)
        data = soup.select('#main > div > div.mtop.firstMod.clearfix > div.leftBox > div:nth-child(2) > ul > li > a')
        for i in data:
            result = {
                "title": i.get_text(),
                "url": i.get('href')
            }
            result = json.dumps(result, ensure_ascii=False)    #ensure_ascii=False解决中文乱码
            print(result)
            with open(self.path, 'a', encoding="utf-8") as e:
                e.write(result + '\n')

    def test_reptile_post(self, word=None):
        """
        POST 的请求获取数据的方式不同于 GET，POST 请求数据必须构建请求头才可以
        :return:
        """
        form_data = {
            'i': word,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': '15772629039359',
            'sign': '2d8ceb61adcd6a201c730c8cd44015c3',
            'ts': 1577262903935,
            'bv': '42160534cfa82a6884077598362bbc9d',
            'doctype': 'json',
            'version': 2.1,
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION'
        }
        r = requests.post(self.url2, data=form_data)
        result = json.loads(r.text)
        print(result)


if __name__ == "__main__":
    Myreptile().test_reptile_post('sjfi')
