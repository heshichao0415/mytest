import unittest
from models.myunit import mytest
import os
from configpath import getpath

path = os.path.join(getpath(), 'Case\\XY')
class RunAllClass(object):
    def __init__(self):
        pass

    def run_module(self):
        """
        运行单个模块
        :param moduleName:
        :return:
        """

        # suite = unittest.TestSuite()
        # suite.addTest(mytest.parametrize(moudlename, param=None))
        # runner = unittest.TextTestRunner(verbosity=1)   #执行测试用例集 ,,verbosity 有 0 1 2 三个级别，verbosity=2 的输出最详细
        # result = runner.run(suite)           #失败用例列表
        # print(result)
        # print('sadf')
        discover = unittest.defaultTestLoader.discover(path, pattern="*_st.py")
        runner = unittest.TextTestRunner()
        runner.run(discover)

if __name__ == '__main__':
    RunAllClass().run_module()
