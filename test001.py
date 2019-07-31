
import pymysql

#连接数据库
conn = pymysql.connect(host='127.0.0.1',
                user='root',
                password='newpass',
                db='guest',
                charset='utf8mb4',
                       )


# try:
#     curs = conn.cursor()
#     curs.execute("SELECT realname,phone,email,sign FROM sign_guest WHERE phone='15882438601';")
#     print('ok')
# except:
#     print('error')
# cus = conn.cursor()
# sql = "SELECT realname,phone,email,sign FROM sign_guest WHERE phone='15882438601';"
# try:
#     cus.execute(sql)
#     result = cus.fetchone()
#     print('ok')
# except:
#     print('error')
# finally:
#     conn.close()