import os
import platform
import unittest
import time
import json
import sys
import threading
from read_writeyaml import MyYaml
from myloging import Loging
from write_readini import write_ini, read_ini
from models.myunit import mytest
from models.myunit_per import ReadYaml
from models.MyRedis import Myredis as redis
from configpath import getpath

pathh = os.path.join(getpath(), 'result', 'report.html')


log = Loging()
redis = redis()
path = getpath()

class myThread(threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, module, times):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.module = module
        self.time = times

    def run(self):
        time.sleep(self.time)
        log.info('开启线程:{}'.format(self.name))
        RunAllClass().run_module(self.module)  #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数

    def __del__(self):
        log.info('{}线程结束！'.format(self.name))

class RunAllClass(object):
    def __init__(self):
        pass

    def run_module(self, moudleName):
        """
        运行单个模块
        :param moduleName:
        :return:
        """
        suite = unittest.TestSuite()
        suite.addTest(mytest.parametrize(moudleName, param=None))
        runner = unittest.TextTestRunner(verbosity=1)   #执行测试用例集 ,,verbosity 有 0 1 2 三个级别，verbosity=2 的输出最详细
        result = runner.run(suite)
        if result.failures:                   #失败用例
            failures_list = []                #失败用例列表
            for i in result.failures:
                case_id = str(i[0]).split('(')[0]
                case_info = str(i[1])
                failures_list.append([case_id, case_info])
            redis.case_failures(failures_list)
        if result.errors:
            errors_list = []
            for i in result.errors:
                case_id = str(i[0]).split('(')[0]
                case_info = str(i[1])
                errors_list.append([case_id, case_info])
            redis.case_errors(errors_list)
        if result.skipped:
            skipped_list = []
            for i in result.skipped:
                case_id = str(i[0]).split('(')[0]
                case_info = str(i[1])
                skipped_list.append([case_id, case_info])
            redis.case_skipped(skipped_list)

class AllResult(object):
    """所有执行结果"""

    def __init__(self):
        redis.remove_redis([
            'all_module',
            'case_data',
            'case_failures',
            'case_errors',               #删除数据
            'case_skipped',
        ])
        self.timeout = MyYaml().config('timeout')
        self.projectName = MyYaml().config('projectName')
        self.EnvName = MyYaml().config('EnvName')    #生产环境
        self.moudleName = MyYaml().config('moudleName')    # all
        if self.moudleName is None:
            self.moudleName = ''
        self.matching = MyYaml().config('matching')        #正则
        self.ip = MyYaml().config('ip')
        self.domain = MyYaml().config('domain')     #本地测试环境
        self.app_config = MyYaml().interface_data
        if self.domain is None:
            self.get_url = 'http://{}/polls/get_report/'.format(self.ip)
        else:
            self.get_url = 'http://{}/polls/get_report/'.format(self.domain)
        self.message = MyYaml().config('message')

        def moudle_name():
            """
            获取可运行模块
            :return: moudle list
            """
            moudleName = MyYaml().config('moudleName')
            project_names = os.path.join(path,'{}'.format(self.projectName))
            dir_list = os.listdir(project_names)  #os.listdir(project_names):列出paoject_names下的目录和文件
            moudle_list = []  #一级目录, XY
            all_import_class = []  #所有要导入的测试类
            all_moudle = []     #所有的类名
            if moudleName is None:         #运行所有模块
                for i in dir_list:
                    if '.' not in i and '__' not in i:
                        if os.path.exists(project_names + '/{}/__init__.py'.format(i)):    #判断路径是否存在
                            moudle_list.append(i)
            else:
                if os.path.exists(project_names + '/{}/__init__.py'.format(moudleName)):     #运行指定模块
                    moudle_list.append(moudleName)
            for a in moudle_list:           #模块
                dir_name = project_names + '\\' + a
                dir_list = os.listdir(dir_name)      #os.listdir()用于返回指定文件夹中包含的文件或文件夹列表
                for b in dir_list:
                    if self.matching.split('_')[1] in b:    #筛选出测试用例
                        import_name = '{}_{}'.format(b.split('_')[0], a)           #类名
                        all_import_class.append('from.{}.{} import {}'.format(a, b.split('.')[0], import_name))   #所有要导入的测试类
                        all_import_class.append('\n')
                        all_moudle.append(import_name)
            init_file_py = project_names + '/__init__.py'
            if os.path.exists(init_file_py):        #os.path.exists(init_file_py):判断是否存在文件或目录init_file_py
                os.remove(init_file_py)     #os.remove(file):删除一个文件
            all_moudle = str(all_moudle)   #类名
            import re
            all_moudle = re.sub("'", '', all_moudle)    #sub()：替换
            with open(init_file_py, 'w') as f:         #测试类写入__init__.py文件
                f.writelines(all_import_class)
                f.write('moudle_list = {}'.format(all_moudle))
                f.write('\n')
                f.close()
            return all_moudle, moudle_list   #all_moudle=所有类名（模块），moudle_list=ZY包下的所有包
        self.all_moudle, self.moudle_list = moudle_name()         #调用并赋值

    def run_class(self):
        from Case import moudle_list
        redis.all_module(moudle_list)     #存进redis
        #创建新线程
        count = 0
        numbers = 0
        if len(redis.read_moudle('all_module')) != 0:    #计算长度，len长度，所有的测试用例多少个
            while True:       #循环
                log.info('共计{}个测试类'.format(len(redis.read_moudle('all_module'))))
                if len(redis.read_moudle('all_module')) != 0:
                    threads = []
                    log.info('添加线程')
                    try:
                        moudle = redis.rpop('all_module', MyYaml().config('thread_count'))
                        moudle_per = ReadYaml().return_module(moudle_list, moudle)
                        for i in moudle_per:
                            threads.append(myThread(count, "Thread-{}".format(count), i, 0))    #一次性开启的线程数量
                            count += 1
                    except Exception:
                        pass
                    #开启新线程
                    for i in threads:
                        try:
                            i.start()   #start开启线程
                        except Exception:
                            pass
                    #等待所有线程完成
                    for t in threads:
                        try:
                            t.join()    #等待线程、子线程完毕后关闭主线程
                        except Exception:
                            pass
                    log.info('主进程{}结束'.format(numbers))
                    numbers += 1                   #主进程
                else:
                    log.info('所有主进程结束！')
                    break
        else:
            log.info('测试集为空')

    def results_collected(self):
        """
        结果收集
        :return:
        """
        all_cases = []
        all_times = []
        timeout_cases = []
        right_cases = []
        fail_cases = []
        fail_error_cases = []
        right_fail_cases = []
        error_cases = []
        skip_cases = []
        case_infos_list = redis.rpop('case_data')     #移除返回右边最后一个元素，lpop删除返回左边列表第一个，（测试用例数据）
        case_errors_list = redis.rpop('case_errors')
        case_failures_list = redis.rpop('case_failures')
        case_skipped_list = redis.rpop('case_skipped')
        all_test_fun = ReadYaml().case_info_data(self.all_moudle)
        for case_ins in all_test_fun:
            case_info = {'case_name': case_ins[1]['case_name'], 'mode': case_ins[1]['mode'],
                         'api_url': case_ins[1]['url'],
                         'time': 0, 'statues': '', 'info': ''}
            for e in case_failures_list:
                e = list(eval(e))   #列表转换 ， eval
                if case_ins[0] == e[0]:
                    case_info['statues'] = 'fail'
                    break
            for f in case_errors_list:
                f = list(eval(f))
                if case_ins[0] == f[0]:
                    case_info['statues'] = 'error'
                    case_info['info'] = f[1]
                    break
            for h in case_skipped_list:
                if case_ins[0] == h[0]:
                    case_info['statues'] = 'skip'
                    case_info['info'] = h[1]  # 'No Response'
                    break
            if case_info['statues'] == '':
                case_info['statues'] = 'pass'
            for i in case_infos_list:
                i = list(eval(i))
                if i[0] == case_ins[0]:
                    if case_info['statues'] == 'pass':
                        case_info['info'] = i[1]
                        try:
                            json_data = float(json.loads(i[1])['time_count'])
                        except Exception:
                            json_data = 0
                        case_info['time'] = float('%.2f' % json_data)
                        all_times.append(json_data)
                    elif case_info['statues'] == 'fail':
                        case_info['info'] = i[1]
                        try:
                            json_data = float(json.loads(i[1])['time_count'])
                        except Exception:
                            json_data = 0
                        case_info['time'] = float('%.2f' % json_data)
                        all_times.append(json_data)
                    else:
                        break
            case_infos = [
                self.projectName,
                case_ins[0],
                case_info['case_name'],
                case_info['api_url'],
                case_info['mode'],
                case_info['time'],  # 11-23
                case_info['statues'],
                '详细',
                case_info['info'],
            ]
            all_cases.append(case_infos)
        for g in all_cases:
            if g[-3] == 'pass':
                right_cases.append(g)
                right_fail_cases.append(g)
            elif g[-3] == 'fail':
                fail_cases.append(g)
                fail_error_cases.append(g)
                right_fail_cases.append(g)
            elif g[-3] == 'error':
                error_cases.append(g)
                fail_error_cases.append(g)
            else:
                skip_cases.append(g)
        for timeout in right_fail_cases:
            if timeout[-4] > self.timeout:
                timeout_cases.append(timeout)
        dmps = MyYaml().baseData('report_cases')
        dmps['all_cases'] = all_cases
        dmps['right_cases'] = right_cases
        dmps['fail_cases'] = fail_cases
        dmps['error_cases'] = error_cases
        dmps['untreaded_cases'] = skip_cases
        fail_error_cases.sort(key=lambda x: (x[5]), reverse=True)
        dmps['fail_error_cases'] = fail_error_cases
        timeout_cases.sort(key=lambda x: (x[5]), reverse=True)
        dmps['timeout_cases'] = timeout_cases
        return dmps, all_times

    def run_all_case(self):
        now_time = time.strftime('%Y-%m-%d %H:%M:%S')             #获取时间并转换为易读格式time.strftime
        log.debug('now_time:{}'.format(now_time))
        startTime = time.time()
        self.run_class()  # 运行所有模块
        stopTime = time.time()
        timeTaken = '%d秒' % (stopTime - startTime)
        end_time = time.strftime('%Y-%m-%d %H:%M:%S')
        dmps, all_times = self.results_collected()  # 收集结果
        try:
            max_times = '%.2f' % max(all_times)
        except Exception as msg:
            max_times = '0'
            log.debug(msg)
        try:
            aver_time = '%.2f' % (sum(all_times) / len(all_times))
        except Exception as msg:
            aver_time = '0'
            log.debug(msg)
        try:
            min_time = '%.2f' % min(all_times)
        except Exception as msg:
            min_time = '0'
            log.debug(msg)
        test_info = [now_time,
                        end_time,
                        timeTaken,
                        max_times,
                        aver_time,
                        min_time,
                        ]
        dmps['test_info'] = test_info
        dmps['env_sign'] = self.EnvName
        # self.get_report(
        #     dmp=dmps,
        #     all_cases=dmps['report_cases']['all_cases'],
        #     fail_error_cases=dmps['report_cases']['fail_error_cases'],
        #     timeout_cases=dmps['report_cases']['timeout_cases']
        # )  # 发送测试报告
        # log.info('django登录超时')

if __name__ == '__main__':
    AllResult().run_all_case()






















































