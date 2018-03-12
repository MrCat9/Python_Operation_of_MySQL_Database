#数据访问层-->访问-->数据库



#python DB API --> python访问数据库的统一接口规范

#python程序<---->数据库服务器
#数据库连接对象connection  用于连接python程序与数据库服务器
#数据交互对象cursor  用于交互数据
#数据库异常类exceptions

#创建connection-->获取cursor-->执行查询、执行命令、获取数据、处理数据-->关闭cursor-->关闭connection

#pip install PyMySQL  -->安装pymysql
#测试是否安装成功：
import pymysql
print(pymysql)  #<module 'pymysql' from '……路径……'>

#安装MySQL  安装sqlyog



#DB API- 数据库连接对象connection
#连接对象:建立Python客户端与数据库的网络连接
#创建方法: MySQLdb.Connect(参数)
参数名   类型    说明
host    字符串   MySQL服务器地址
port    数字     MySQL服务器端口号
user    字符串   用户名
passwd  字符串   密码
db      字符串   数据库名称
charset 字符串   连接编码

#connection对象支持的方法
方法名       说明    
cursor()    使用该连接创建并返回游标
commit()    提交当前事务
rollback()  回滚当前事务
close()     关闭连接



#
import pymysql
conn = pymysql.connect(
    host = '127.0.0.1',    #指定本地MySQL地址
    port = 3306,
    user = 'root',
    passwd = '123456',
    db = 'pymysql_test_01',
    charset = 'utf8'
    )

cursor = conn.cursor()
print(conn)  #<pymysql.connections.Connection object at 0x0000027B8CEC7898>
print(cursor)  #<pymysql.cursors.Cursor object at 0x0000027B8D442BE0>

cursor.close()
conn.close()
