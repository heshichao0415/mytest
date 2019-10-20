import pymysql
from read_writeyaml import MyYaml
from myloging import Loging
import redis
import json

yaml = MyYaml()
log = Loging()



class Mysql_db():
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.ip = yaml.mysql('ip')
        self.username = yaml.mysql('username')
        self.pwd = yaml.mysql('pwd')
        self.TESTDB = yaml.mysql('TESTDB')
        self.real_sql = yaml.sql('search_results')
        self.redis_ip = MyYaml().config('redis_ip')
        self.redis_port = MyYaml().config('port')
        self.name = MyYaml().config('redis')

    def connect_mysql(self):
        try:
            self.connection = pymysql.connect(
                self.ip,
                self.username,
                str(self.pwd),
                self.TESTDB,
                charset='utf8'
            )
            log.info('链接数据库%s成功' % self.TESTDB)

        except pymysql.err.OperationalError as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def main_redis(self):
        #链接redis
        try:
            pool = redis.ConnectionPool(host=self.redis_ip, port=self.redis_port, decode_responses=True, db=0)
            self.r = redis.StrictRedis(connection_pool=pool)

        except Exception as e:
            print('redis链接失败，error:', e)
        # 从Redis里提取数据
        result = self.r.lrange('zytest_case_data', 0, -1)
        for a in result:
            if not isinstance(a, list):
                result_list = eval(a)
                data = result_list[1]
                data_dict = eval(data)
                self.time_count = data_dict['time_count']
                self.result_data = json.dumps(data_dict['Results'], ensure_ascii=False)     #ensure_ascii=False解决中文乱码问题
                self.case_data = json.dumps(data_dict['parameter'], ensure_ascii=False)    #存入字典类型时，要转化成字符串
                self.case_code = data_dict['expected']
                self.result_code = data_dict['actual']
                self.info_name = result_list[0]
                self.case_name = data_dict['name']
                self.api_address = data_dict['address']
                self.method = data_dict['method']
            #插入mysql
            try:
                sql = '''INSERT INTO sign_detail(name, case_number, case_name, aip_address, aip_method,
                 test_result, case_detail, case_data, result_data, time_count)
                VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')''' % \
                      (self.name, self.info_name, self.case_name, self.api_address, self.method, 1, '详细', self.case_data,
                       self.result_data, self.time_count)
                curs = self.connection.cursor()
                curs.execute(sql)
                self.connection.commit()
                log.info('数据库%s数据插入成功' % self.TESTDB)

            except Exception as msgs:
                print('执行sql语句失败！error:', msgs)

    def db_close(self):
        self.connection.close()  #  断开连接


if __name__ == '__main__':
    a = Mysql_db()
    a.connect_mysql()
    a.main_redis()





