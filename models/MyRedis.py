
import json
import redis
from myloging import Loging
from read_writeyaml import MyYaml
import os, sys
env = os.path.dirname(__file__)
sys.path.append(env)

class Myredis(object):
    def __init__(self):
        redis_ip = MyYaml().config('redis_ip')
        redis_port = MyYaml().config('port')
        pool = redis.ConnectionPool(host=redis_ip, port=redis_port, decode_responses=True, db=0)
        self.r = redis.Redis(connection_pool=pool)
        # Loging().info('链接redis成功')
        self.env = MyYaml().config('env')
        self.log = Loging()

    def all_times(self, all_times):
        """
        从左边插入用例时间
        :param all_time:
        :return:
        """
        self.r.lpush('{}_all_times'.format(self.env), all_times)
        Loging().info('成功插入用例时间')

    def all_cases(self, all_cases):
        """
        所有用例数据
        :return:
        """
        self.r.lpush('{}_all_cases'.format(self.env), json.dumps(all_cases))  #json.dumps编译成json字符串
        Loging().info('插入数据成功')

    def timeout_cases(self, timeout_cases):
        """
        超时用例
        :return:
        """
        self.r.lpush('{}_timeout_cases'.format(self.env), json.dumps(timeout_cases))

    def right_cases(self, right_cases):
        """
        正确用例数据
        :return:
        """
        self.r.lpush('{}_right_cases'.format(self.env), json.dumps(right_cases))

    def fail_cases(self, fail_cases):
        """
        失败用例数据
        :return:
        """
        self.r.lpush('{}_fail_cases'.format(self.env), json.dumps(fail_cases))

    def error_cases(self, error_cases):
        """
        错误用例数据
        :return:
        """
        self.r.lpush('{}_error_cases'.format(self.env), json.dumps(error_cases))

    def fail_error_cases(self, fail_error_cases):
        """
        失败和错误用例数据
        :return:
        """
        self.r.lpush('{}_fail_error_cases'.format(self.env), json.dumps(fail_error_cases))

    def skip_cases(self, skip_cases):
        """
        跳过用例数据
        :return:
        """
        self.r.lpush('{}_skip_cases'.format(self.env), json.dumps(skip_cases))

    def dmp(self, dmp):
        """
        测试报告用例数据
        :return:
        """
        self.r.lpush('{}_dmp'.format(self.env), json.dumps(dmp))

    def case_data(self, case_data):
        """
        测试用例数据
        :return:
        """
        self.r.lpush('{}_case_data'.format(self.env), str(case_data))

    def case_failures(self, case_failures):
        """
        case failures
        :return:
        """
        if len(case_failures) != 0:
            for i in case_failures:
                self.r.lpush('{}_case_failures'.format(self.env), str(i))

    def case_errors(self, case_errors):
        """
        case errors
        :return:
        """
        if len(case_errors) != 0:
            for i in case_errors:
                self.r.lpush('{}_case_errors'.format(self.env), str(i))

    def case_skipped(self, case_skipped):
        """
        case skipped
        :return:
        """
        if len(case_skipped) != 0:
            for i in case_skipped:
                self.r.lpush('{}_case_skipped'.format(self.env), str(i))

    def all_module(self, all_module):
        """
        所有测试模块
        :return:
        """
        if len(all_module) > 0:
            for i in all_module:
                self.r.lpush('{}_all_module'.format(self.env), str(i))

    def rpop(self, module, count=0):
        """
        删除并返回结果
        :return:
        """
        module_list = []
        if count != 0:
            for i in range(count):

                modules = self.r.rpop('{}_{}'.format(self.env, module))  #删除并返回列表最后一个值，当列表不存在时返回None
                if modules is not None:
                    module_list.append(modules)
            return module_list
        else:
            while True:
                modules = self.r.rpop('{}_{}'.format(self.env, module)) #删除并返回列表最后一个值，当列表不存在时返回None
                if modules is not None:
                    module_list.append(modules)
                else:
                    break
            return module_list

    def redis_data(self, all_times):
        """
        返回该字段列表所有数据
        :param all_times:
        :return:
        """
        data = self.r.lrange('{}_{}'.format(self.env, all_times), 0, -1) #返回列表中的所有元素
        if len(data) >= 1:
            return_list = []
            for i in data:
                json_data = json.loads(i)  #解码json数据
                return_list.append(json_data)
            return return_list
        else:
            return data

    def read_moudle(self, all_times):
        """
        返回该字段列表所有数据
        :param all_times:
        :return:
        """
        data = self.r.lrange('{}_{}'.format(self.env, all_times), 0, -1) #返回所有元素
        if len(data) >= 1:
            return_list = []
            for i in data:
                return_list.append(i)
            return return_list                        #返回测试类的列表
        else:
            return data

    def dmp_data(self):
        json_data = MyYaml().baseData('data')
        data = self.r.lrange('{}_dmp'.format(self.env), 0, -1)  #返回所有元素
        all_cases = []
        right_cases = []
        fail_cases = []
        error_cases = []
        untreaded_cases = []
        fail_error_cases = []
        timeout_cases = []
        if len(data) >= 1:
            for i in data:
                json_load = json.loads(i)
                for a in json_load['report_cases']['all_cases']:
                    if a not in all_cases:
                        all_cases.append(a)
                for b in json_load['report_cases']['right_cases']:
                    if b not in right_cases:
                        right_cases.append(b)
                for c in json_load['report_cases']['fail_cases']:
                    if c not in fail_cases:
                        fail_cases.append(c)
                for d in json_load['report_cases']['error_cases']:
                    if d not in error_cases:
                        error_cases.append(d)
                for e in json_load['report_cases']['untreaded_cases']:
                    if e not in untreaded_cases:
                        untreaded_cases.append(e)
                for f in json_load['report_cases']['fail_error_cases']:
                    if f not in fail_error_cases:
                        fail_error_cases.append(f)
                for g in json_load['report_cases']['timeout_cases']:
                    if g not in timeout_cases:
                        timeout_cases.append(g)
            json_data['report_cases']['all_cases'] = all_cases
            json_data['report_cases']['right_cases'] = right_cases
            json_data['report_cases']['fail_cases'] = fail_cases
            json_data['report_cases']['error_cases'] = error_cases
            json_data['report_cases']['untreaded_cases'] = untreaded_cases
            json_data['report_cases']['fail_error_cases'] = fail_error_cases
            json_data['report_cases']['timeout_cases'] = timeout_cases
            return json_data, all_cases, right_cases, fail_cases, \
                   error_cases, untreaded_cases, fail_error_cases, timeout_cases
        else:
            return data

    def remove_redis(self, field):
        """
        删除字段
        :return:
        """
        if isinstance(field, list):   #判断是否为列表，isinstance() 函数来判断一个对象是否是一个已知的类型，类似 type()
            for i in field:
                self.r.delete('{}_{}'.format(self.env, i))  #delete(name),根据删除redis中的任意数据类型（string、hash、list、set、有序set）
        else:
            self.r.delete('{}_{}'.format(self.env, field))


if __name__ == '__main__':
    data = Myredis()
    my = data.rpop('case_data')
    data.all_times('2341')
    print(len(my))
    print(my)






