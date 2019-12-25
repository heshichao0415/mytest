import urllib.request
from bs4 import BeautifulSoup
import re
import chardet
import os
from configpath import getpath
from read_writeyaml import MyYaml

class My_reptile(object):

    def __init__(self):
        self.url = MyYaml().reptile('url')
        self.matching = MyYaml().reptile('matching')
        self.path_images = os.path.join(getpath(), 'images')
        self.path_file = os.path.join(getpath(), 'Py_file', 'test.txt')
        self.method = MyYaml().reptile('method')

    def test_reptile_images(self):
        pass


    def test_reptile_file(self):
        print(self.path_file)
        html = urllib.request.urlopen(self.url).read() #获取网页源代码
        # html = html.decode("gbk") #转成该网站格式
        # print(chardet.detect(html)) #打印返回网页的编码方式
        chardit1 = chardet.detect(html)     #获取网站编码格式
        html = html.decode(chardit1['encoding'])             #转换为网站编码格式
        reg = self.matching
        reg = re.compile(reg)
        urls = re.findall(reg, html)
        for url in urls:
            chapter_url = url[0]  # 章节路径
            chapter_title = url[1]  # 章节名
            chapter_html = urllib.request.urlopen(chapter_url).read()  # 获取该章节的全文代码
            chapter_html = chapter_html.decode(chardit1['encoding'])
            chapter_reg = r'</script>&nbsp;&nbsp;&nbsp;&nbsp;.*?<br />(.*?)<script type="text/javascript">'  # 匹配
            chapter_reg = re.compile(chapter_reg, re.S)
            chapter_content = re.findall(chapter_reg, chapter_html)
            for content in chapter_content:
                content = content.replace("&nbsp;&nbsp;&nbsp;&nbsp;", "")  # 使用空格代替
                content = content.replace("<br />", "")  # 使用空格代替
                f = open(self.path_file, 'w')  # 保存到本地
                f.write(content)

if __name__ == "__main__":
    My_reptile().test_reptile_file()
