import requests
from bs4 import BeautifulSoup
import re
from configpath import getpath
import os
path = os.path.join(getpath(), 'Py_file', 'test.txt')
print(path)

url = 'http://www.cntour.cn/'
strhtml = requests.get(url)

soup = BeautifulSoup(strhtml.text, 'lxml')

data = soup.select('#main>div>div.mtop.firstMod.clearfix>div.centerBox>ul.newsList>li>a')

for item in data:
    result = {
        'title': item.get_text(),        #提取标签的正文用 get_text() 方法
        'link': item.get('href'),         #提取标签中的 href 属性用 get() 方法
        'ID': re.findall('\d+', item.get('href'))
    }
    write = str(result) + '\n'
    with open(path, 'a', encoding='utf-8') as e:
        e.write(write)