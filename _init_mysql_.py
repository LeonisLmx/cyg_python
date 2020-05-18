# 导入pymysql模块
import pymysql

# 连接database
conn = pymysql.connect("localhost", "root", "123456", "cyg")
# 得到一个可以执行SQL语句的光标对象
cursor = conn.cursor()
# 定义要执行的SQL语句
sql = """
# select * from article_description where author = '刘明新'
# """
# 执行SQL语句
cursor.execute(sql)

# data = cursor.fetchall()
#
# for row in data:
#     print(str(row))

# 关闭光标对象
cursor.close()
# 关闭数据库连接
conn.close()


def execute(sql):
    conn = pymysql.connect("localhost", "root", "123456", "cyg")
    # 得到一个可以执行SQL语句的光标对象
    cursor = conn.cursor()
    cursor.execute(sql)
