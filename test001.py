#
# import pymysql
# from read_writeyaml import MyYaml
# from myloging import Loging
# import json
#
# yaml = MyYaml()
# log = Loging()
#
#
# class Mysql_db():
#     def __init__(self, **kwargs):
#         self.kwargs = kwargs
#         self.ip = yaml.mysql('ip')
#         self.username = yaml.mysql('username')
#         self.pwd = yaml.mysql('pwd')
#         self.TESTDB = yaml.mysql('TESTDB')
#         self.real_sql = yaml.sql('search_results')
#         self.redis_ip = MyYaml().config('redis_ip')
#         self.redis_port = MyYaml().config('port')
#
#     def connect_mysql(self):
#         try:
#             self.connection = pymysql.connect(
#                 self.ip,
#                 self.username,
#                 str(self.pwd),
#                 self.TESTDB,
#                 charset='utf8'
#             )
#             log.info('链接数据库%s成功' % self.TESTDB)
#         except pymysql.err.OperationalError as e:
#             print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
#     def main_redis(self):
#         result = ['[\'test_auth_ZYAccessToken\', \'{\\n    "actual": 422,\\n    "Results": {\\n        "code": 422,\\n        "message": "验证码已过期"\\n    },\\n    "time_count": "0.461918",\\n    "parameter": {\\n        "code": "1234",\\n        "os": "ios",\\n        "mobile": "15882438611"\\n    },\\n    "expected": 200\\n}\']', '[\'test_login_token\', \'{\\n    "parameter": {\\n        "pass": "yRZN3XBoKWV5p2zm9Pf7ICDA8xQdghOk",\\n        "account": "61AAF941-1385-A83E-12C0-F9A2C41B1C1E"\\n    },\\n    "expected": 200,\\n    "Results": {\\n        "message": "访问资源URI不存在",\\n        "once": "yoQwJH",\\n        "timestamp": 1566654211,\\n        "code": 404\\n    },\\n    "time_count": "0.143196",\\n    "actual": 404\\n}\']']
#         for a in result:
#             if not isinstance(a, list):
#                 result_list = eval(a)
#                 data = result_list[1]
#                 data_dict = eval(data)
#                 print(data_dict)
#                 self.time_count = data_dict['time_count']
#                 self.result_data = json.dumps(data_dict['Results'], ensure_ascii=False)  # ensure_ascii=False解决中文乱码问题
#                 self.case_data = json.dumps(data_dict['parameter'], ensure_ascii=False)  # 存入字典类型时，要转化成字符串
#                 self.case_code = data_dict['expected']
#                 self.result_code = data_dict['actual']
#                 self.info_name = result_list[0]
#                 sql = '''INSERT INTO sign_detail(name, case_number, case_name, aip_address, aip_method, test_result, case_detail, case_data, result_data, time_count)
#                 VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')''' % (
#                 'SCRM', self.info_name, '获取验证码', 'api/login/v3/acctoken', 'post', 1, '详细', self.case_data, self.result_data,
#                 self.time_count)
#                 curs = self.connection.cursor()
#                 curs.execute(sql)
#                 self.connection.commit()
#                 print('mysql数据插入成功')
#
#
#     def db_close(self):
#         self.connection.close()  # 断开连接
#
#
# if __name__ == '__main__':
#     a = Mysql_db()
#     a.connect_mysql()
#     a.main_redis()

import re

a = "['/api/v1/xyhw/GetGameList', {'openID1': '', 'openID2': '', 'top': '', 'time': '', 'sign': ''}, [200], 'post', {}]"
c = re.sub("openID1': ''", "openID1': 'sfsfkh'", a)
print(c)