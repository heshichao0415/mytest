import time
import logging
import os
import sys
from read_writeyaml import MyYaml
import configpath

yaml = MyYaml()

class Loging:
    """日志"""
    def __init__(self, level=yaml.log('level'), logger_name='hsc'):
        self.logger = logging.getLogger(logger_name)  # # 获取logger实例，如果参数为空则返回root logger、创建一个logger
        if not self.logger.handlers:
            formatter = logging.Formatter(  # 指定logger输出格式
                '时间:%(asctime)s '  # 时间，默认精确到毫秒
                # '文件名:%(filename)s ' # 日志文件名
                # '模块名:%(module)s ' #日志模块名
                # '方法:%(funcName)s '  # 日志函数名
                # '代码行:%(lineno)d ' # 日志模块代码行
                '级别:%(levelname) s '  # log级别
                # '路径:%(pathname)s ' # 完整路径
                '消息：%(message)s'  # 打印的消息
            )
            current_data = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 当前系统日期
            log_name = '{}.log'.format(current_data)  # 每天一份日志
            log_file = os.path.join(configpath.getpath(), 'logs/{}'.format(log_name))  # log路径
            file_handler = logging.FileHandler(log_file, encoding='utf-8')  # 文件日志
            file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
            self.console_handler = logging.StreamHandler(sys.stdout)  # 控制台日志
            self.console_handler.setFormatter(formatter)  # 也可以直接给formatter赋值
            self.logger.addHandler(self.console_handler)  # 为logger添加的日志处理器
            self.logger.addHandler(file_handler)  # 为logger添加的日志处理器
            self.logger.setLevel(level)  # log级别（NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL对应的值分别为：0,10,20,30,40,50）

    def debug(self, content):
        """输出不同级别的log"""
        self.fontColor('\033[0;32m%s\033[0m')
        self.logger.debug(content)

    def info(self, content):
        self.fontColor('\033[0;34m%s\033[0m')
        self.logger.info(content)

    def warning(self, content):
        self.fontColor('\033[0;37m%s\033[0m')
        self.logger.warning(content)

    def error(self, content):
        self.fontColor('\033[0;31m%s\033[0m')
        self.logger.error(content)

    def fontColor(self, color):
        #不同的日志输出不同的颜色
        formatter = logging.Formatter(color % '[%(asctime)s] - [%(levelname)s] - %(message)s')
        self.console_handler.setFormatter(formatter)
        self.logger.addHandler(self.console_handler)



if __name__ == '__main__':
    log = Loging()
    log.debug('heshichao')
    log.info('dfddfddddddddddddd')
    log.error('2222222222222222222222222')
    log.warning('afasfsfsdf')




