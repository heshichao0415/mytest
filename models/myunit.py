import unittest
import json
from myloging import Loging
from read_writeyaml import MyYaml
from .MyRedis import Myredis
from .result import results
from write_readini import read_ini

redis = Myredis()

def case_id():
    global case_count
    case_count += 1
    if case_count <= 9:
        count = "00" + str(case_count)
    elif case_count <= 99:
        count = "0" + str(case_count)
    else:
        count = str(case_count)
    return count

def getTimeCount(time):
    if '[' in time:
        _time = 0
    elif len(time) > 10:
        _time = 0
    else:
        _time = time
    return _time


class mytest(unittest.TestCase):
    def __init__(self, methodName='runTest', param=None):
        super(mytest, self).__init__(methodName)
        self.param = param

    log = Loging()
    result = None
    global case_count
    case_count = 0

    @classmethod
    def setUpClass(self):
        self.key_list = {

        }

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        self.className = self.__class__.__name__
        self.module = self.__class__.__module__
        self.case_info = self._testMethodName  #接口方法名、self._testMethodName用来获取方法名
        self.key = self.className.split('_')[1]
        self.datas = MyYaml().interface_data[self.key]
        self.data = []
        self.case_name = []
        for i in self.datas:
            if i['className'] == self.className:
                self.data.append(i['url'])  # api地址   0
                for j in i['funName']:
                    for k in j.keys():
                        if k == self.case_info:
                            self.data.append(j[self.case_info]['bar'])  #参数   1
                            self.data.append(j[self.case_info]['result']) #预期结果    2
                            self.data.append(j[self.case_info]['mode'])       #请求方式   3
                            self.data.append(j[self.case_info]['test_data'])   #接口时间   -1
                            self.case_name.append(i['name'])
        if not isinstance(self.data[1], list):
            self.data[1] = dict(self.data[1], **self.key_list)
        self.url = MyYaml().config('url') + self.data[0]

        try:
            token = read_ini(node='session', child='access_token')    #重配置文件获取token
            # print(token)
        except Exception:
            token = '0'
        self.headers = {'Authorization': 'Bearer{}'.format(token)}   #请求头

    def tearDown(self):
        try:
            parameter = self.result['code']
        except Exception:
            parameter = ''
        try:
            msg = self.result['message']
        except Exception:
            msg = ''

        Response = results(
            name=self.case_name[0],
            expected=self.data[2][0],
            actual=parameter,
            method=self.data[3],
            address=self.data[0],
            parameter=self.data[1],
            Results=self.result,
            time_count=getTimeCount(str(self.data[-1])),     #接口响应时间
        )
        Response = json.dumps(Response, indent=4, ensure_ascii=False)
        #保存redis
        print(Response)
        redis.case_data([self.case_info, Response])                             #测试数据缓存redis
        self.log.debug(
            '%s->%s->%s: 传参：%s 返回结果：%s' % (
                self.module,
                self.className,
                self.case_info,
                self.data[1],
                self.result
            )
        )
        self.log.debug('{} 验证完毕'.format(self.case_name[0]))
        self.assertEqual(parameter, self.data[2][0], msg=msg)
        print("用例执行结束。。。")

    @staticmethod
    def parametrize(testcase_klass, param=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite





