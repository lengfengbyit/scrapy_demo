
import sys
import pymysql.cursors

MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': 'root',
    'db': 'douban',
    'charset': 'utf8'
}

conn = pymysql.connect(
    host = MYSQL_CONFIG['host'],
    port = MYSQL_CONFIG['port'],
    user = MYSQL_CONFIG['user'],
    passwd = MYSQL_CONFIG['passwd'],
    db = MYSQL_CONFIG['db'],
    charset = MYSQL_CONFIG['charset']
)
cursor = conn.cursor()





# sql = "INSERT INTO trade (name, account, saving) VALUES ( '%s', '%s', %.2f )"
# data = ('雷军', '13512345678', 10000)

# print(sql % data)


sys.exit(0)

res = cursor.execute(sql % data)
res2 = conn.commit()

print(res, res2)
