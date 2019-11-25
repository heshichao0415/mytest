from __future__ import unicode_literals
from threading import Timer
import itchat
import requests
# 抓取金山毒霸每日一句，英文和翻译
def get_news():
  url = "http://open.iciba.com/dsapi/"
  r = requests.get(url)
  content = r.json()['content']
  translation = r.json()['translation']
  return content, translation
def send_news():
  try:
    # 把抓取的数据传参
    contents = get_news()
    # 登陆微信账户，扫码登陆
    itchat.auto_login(hotReload=True)
    # 查找你微信号上想要发送人的名称
    my_friend = itchat.search_friends(name=u'。。')
    print('查找成功')
    # 发送消息
    itchat.send(contents[0], toUserName=my_friend)
    itchat.send(contents[1], toUserName=my_friend)
    itchat.send(u"I love you", toUserName=my_friend)
    # 一天循环发送一次
    t = Timer(80, send_news)
    t.start()
  except:
    my_friend = itchat.search_friends(name=u'。。')
    itchat.send(u"今天消息发送失败了", toUserName=my_friend)
if __name__ == '__main__':
  send_news()



