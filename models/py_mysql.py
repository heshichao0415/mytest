import pymysql
from read_writeyaml import MyYaml
from myloging import Loging
import configpath
import os

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

    def connect_mysql(self):
        try:
            self.connection = pymysql.connect(
                self.ip,
                self.username,
                str(self.pwd),
                self.TESTDB
            )
            log.info('链接数据库%s成功' % self.TESTDB)

        except pymysql.err.OperationalError as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))


    def perform_sql(self):
        try:
            curs = self.connection.cursor()

            curs.execute(self.real_sql)
            # for rec in curs.fetchall():
                # log.info('数据库%s查询成功' % self.TESTDB)
                # return rec
                # print(rec)
            log.info('数据库%s查询成功' % self.TESTDB)
            for row in curs.fetchall():
                empno = row[0]
                ename = row[1]
                job = row[2]
                mgr = row[3]
                hiredate = row[4]
                sal = row[5]
                commom = row[6]
                deptno = row[7]
                data = ("empno=%s, ename=%s, job=%s, mgr=%s, hiredate=%s, sal=%s, common=%s, deptno=%s\n"
                     % (empno, ename, job, mgr, hiredate, sal, commom, deptno))
                with open(os.path.join(configpath.getpath(), 'result', 'mysql.txt'), 'a') as f:
                    f.write(data)
                    if row == all(curs.fetchall()):

                        return data

        except Exception as msgs:
            print(msgs)
            print('执行sql语句失败！')

    def db_close(self):
        self.connection.close()  # 断开连接


if __name__ == '__main__':
    a = Mysql_db()
    a.connect_mysql()
    a.perform_sql()





