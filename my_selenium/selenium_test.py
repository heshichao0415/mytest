from selenium import webdriver
import time
import unittest
from myloging import Loging
from selenium.webdriver import ActionChains     #鼠标操作的封装类
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
log = Loging()

class Selenium_test(unittest.TestCase):
    """selenium实践练习"""
    def setUp(self):
        self.dr = webdriver.Chrome()
        self.base_url = "https://www.baidu.com"
        self.base_url1 = "http://news.baidu.com"
        self.base_url2 = "http://www.126.com"
        # 设置元素识别超时时间
        self.dr.implicitly_wait(15)
        # 设置页面加载超时时间
        self.dr.set_page_load_timeout(15)
        # 设置异步脚本加载超时时间
        self.dr.set_script_timeout(15)

    def test_open_chrome(self):
        dr = self.dr
        #访问百度首页
        dr.get(self.base_url)
        #获取元素的尺寸 size
        size = dr.find_element_by_id('kw').size
        log.info('输入框的大小为：{}'.format(size))
        commit_size = dr.find_element_by_id('su').size
        log.info('提交按钮的大小为：{}'.format(commit_size))
        #获取文本信息 text
        text = dr.find_element_by_xpath('//*[@id="u1"]/a[1]').text
        log.info('获取的文本信息为：{}'.format(text))
        #查看元素的属性值 get_attribute()
        attribute = dr.find_element_by_id('kw').get_attribute('name')
        log.info('查看的元素属性值为：%s' % attribute)
        #返回元素是否可见 is_displayed()
        result = dr.find_element_by_id('kw').is_displayed()
        log.info('百度输入框元素kw是否可见：%s' % result)
        #鼠标操作，context_click()右击， double_click()双击， drag_and_drop()拖动， move_to_element()鼠标悬停
        above = dr.find_element_by_link_text('设置')     #定位到要悬停的元素
        ActionChains(dr).move_to_element(above).perform()     #进行悬停操作
        log.info('鼠标悬停到百度操作成功')
        time.sleep(1)
        above1 = dr.find_element_by_link_text('高级搜索')
        ActionChains(dr).move_to_element(above1).perform()     #悬停到二级菜单
        dr.find_element_by_link_text('高级搜索').click()       #鼠标点击二级菜单
        time.sleep(1)
        #获取验证信息  title获取当前页面的标题， current_url获取当前页面的url， text获取当前页面的文本信息
        title = dr.title        #获取当前页面的title
        log.info('当前页面的title为：%s' % title)
        now_url = dr.current_url     #获取当前你页面的url
        log.info('当前页面的url信息为：%s' % now_url)
        #检查某个元素是否存在，不存在则抛出异常
        #webdriverwait类，在设置时间内每隔一段时间检测一次当前页面元素是否存在，超时检测不到则抛出异常
        try:
            #驱动dr，最长超时时长5秒，检测的间隔0.5秒，寻找检测ID为kw的元素
            WebDriverWait(dr, 5, 0.5).until(expected_conditions.visibility_of_element_located((By.ID, 'kw')))
            log.info('kw元素存在')
        except:
            log.error('kw元素不存在')
        #定位一组元素 elements
        dr.find_element_by_id('kw').send_keys('selenium')
        texts = dr.find_elements_by_xpath('//*[@id="s_tab"]/div/a')
        lists = []
        munt = len(texts)
        for i in texts:
            i = i.text
            lists.append(i)
        log.info('定位的%s元素为：%s' % (munt, lists))
       # dr.find_element_by_id('kw').send_keys('迅游科技有限公司')
        #清除文本
        dr.find_element_by_id('kw').clear()
        log.info('clear文本清除成功')
        #访问新闻网页
        dr.get(self.base_url1)
        #dr.maximize_window()     #全屏
        log.info('设置浏览器宽900，高800显示')
        dr.set_window_size(900, 800)   #自定义浏览器的高度和宽度 set_window_size()
        #webdriver提供了back()和forward()方法来模拟后退我前进按钮
        dr.back()    #后退到百度首页
        log.info('成功后退到百度首页')
        dr.forward()    #前进到新闻页面
        log.info('成功前进到新闻页面')
        dr.refresh()          #刷新浏览器 F5
        log.info('刷新浏览器成功')
        #submit提交表单，例如有些搜索框不提供按钮操作，而是通过键盘回车键完成提交，可以使用submit()
        #表单切换 switch_to.frame()
        dr.get(self.base_url2)
        dr.find_element_by_link_text('密码登录').click()
        try:
            #处理动态id表单切换
            #iframe = dr.find_element_by_css_selector('iframe[id^="x-URS-iframe"]')      #通过css定位动态ID
            iframe = dr.find_element_by_xpath('//iframe[starts-with(@id, "x-URS-iframe")]')    #通过xpath定位动态ID，开始
            #iframe = dr.find_element_by_xpath('//*[@id="loginDiv"]/iframe')    #通过iframe上一级来定位
            #iframe = dr.find_element_by_xpath("//iframe[contains(@id, 'x-URS-iframe')]")      #通过xpath定位,中间
            #iframe = dr.find_element_by_xpath("//iframe[ends-with(@id, 'x-URS-iframe')]")      #通过xpath定位,结尾
            dr.switch_to.frame(iframe)     #切换表单
            log.info('动态id表单切换成功')
        except:
            log.error('表单切换失败')
        dr.find_element_by_name('email').send_keys("username")
        dr.find_element_by_name('password').send_keys('password')
        dr.find_element_by_id('dologin').click()
        time.sleep(1)
        #多窗口切换
        dr.get(self.base_url)
        dr.find_element_by_id('kw').send_keys('selenium')
        dr.find_element_by_id('su').click()
        search_windows = dr.current_window_handle      #获取当前窗口句柄
        dr.find_element_by_xpath('//*[@id="2"]/h3/a').click()
        windows = dr.window_handles     #获取当前所有打开的窗口句柄
        # dr.switch_to.window(windows[-1])     #切换到新的窗口
        # text = dr.find_element_by_xpath('//*[@id="__next"]/div[1]/div/div/section[1]/article/h1[1]').text
        # if text == '什么是selenium':
        #     log.info('窗口切换成功')
        # else:
        #     log.error('窗口切换失败')

        #第二种方法
        for i in windows:
            if i != search_windows:
                dr.switch_to.window(i)
        text = dr.find_element_by_xpath('//*[@id="__next"]/div[1]/div/div/section[1]/article/h1[1]').text
        if text == '什么是selenium':
            log.info('窗口切换成功')
        else:
            log.error('窗口切换失败')
        search_windows1 = dr.current_window_handle
        dr.find_element_by_link_text('小董不太懂').click()
        windows = dr.window_handles
        for i in windows:
            if i not in (search_windows, search_windows1):
                dr.switch_to.window(i)
        text = dr.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[1]/a').text
        if text == '小董不太懂':
            log.info('切换第三个窗口成功')
        else:
            log.info('切换到第三个窗口失败')
        dr.switch_to.window(search_windows1)     #切换到第二个窗口
        text = dr.find_element_by_xpath('//*[@id="__next"]/div[1]/div/div/section[1]/article/h1[1]').text
        if text == '什么是selenium':
            log.info('切回到第二个窗口成功')
        else:
            log.error('切回到第二个窗口失败')
        #警告弹窗问题处理？？？


    def tearDown(self):
        self.dr.quit()

if __name__ == '__main__':
    unittest.main()
