from selenium import webdriver
import unittest
import time
class BDtest(unittest.TestCase):
    def setUp(self):
        self.url = 'https://www.baidu.com'
        self.dr = webdriver.Chrome()

    def testbaidu(self):
        dr = self.dr
        dr.get(self.url)
        dr.find_element_by_id('kw').send_keys('51testing')
        dr.find_element_by_id('su').click()
        time.sleep(3)

    def tearDown(self):
        self.dr.close()

if __name__ == '__main__':
    unittest.main()