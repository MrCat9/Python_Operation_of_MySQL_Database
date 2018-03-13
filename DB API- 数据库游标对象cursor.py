#DB API- 数据库游标对象cursor
#游标对象:用于执行查询和获取结果
#cursor对象支持的方法:
参数名                 说明
execute(op[,args])    执行一个数据库查询和命令
fetchone()            取的结果集的下一行
fetchmany(size)       获取结果集的下几行
fetchall()            获取结果集中剩下的所有行
rowcount              最近一次execute返回数据的行数或影响行数
close()               关闭游标对象

#execute方法：执行sql、将结果从数据库获取到客户端
客户端                  MySQL服务器
execute（sql）--------> 执行sql
本地缓冲区<------------- 结果

#fetchone()，fetchmany(size)，fetchall()方法：移动rownumber，返回数据



#使用select查询数据
#开始-->创建connection-->获取cursor-->使用cursor.execute()执行select语句
#-->使用cursor.fetch···()获取并出处理数据-->关闭cursor-->关闭connection-->结束

#用sqlyog创建数据库
CREATE TABLE user (
  userid INT(11) NOT NULL AUTO_INCREMENT,
  username VARCHAR(100) DEFAULT NULL,
  PRIMARY KEY (userid)
) ENGINE=INNODB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8

#
import pymysql
conn = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = '123456',
    db = 'pymysql_test01',
    charset = 'utf8'
    )

cursor = conn.cursor()
print(conn)  #<pymysql.connections.Connection object at 0x0000027E41957320>
print(cursor)  #<pymysql.cursors.Cursor object at 0x0000027E41E15AC8>

sql = 'select * from user'  #编写sql语句
cursor.execute(sql)  #用cursor的execute()方法执行sql语句

print(cursor.rowcount)  #9

rs = cursor.fetchone()
print(rs)  #(1, 'name1')

rs = cursor.fetchmany(3)
print(rs)  #((2, 'name2'), (3, 'name3'), (4, 'name4'))

rs = cursor.fetchall()
print(rs)  #((5, 'name5'), (6, 'name6'), (7, 'name7'), (8, 'name8'), (9, 'name9'))

cursor.close()
conn.close()



#
import pymysql
conn = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = '123456',
    db = 'pymysql_test01',
    charset = 'utf8'
    )

cursor = conn.cursor()
print(conn)  #<pymysql.connections.Connection object at 0x0000022D4C667358>
print(cursor)  #<pymysql.cursors.Cursor object at 0x0000022D4CB61BE0>

sql = 'select * from user'
cursor.execute(sql)

print(cursor.rowcount)  #9

rs = cursor.fetchall()
print(rs)
#((1, 'name1'), (2, 'name2'), (3, 'name3'), (4, 'name4'), (5, 'name5'), (6, 'name6'), (7, 'name7'), (8, 'name8'), (9, 'name9'))
for row in rs:
    print('userid=%s, username=%s'%row)  #

cursor.close()
conn.close()
#userid=1, username=name1
#userid=2, username=name2
#userid=3, username=name3
#userid=4, username=name4
#userid=5, username=name5
#userid=6, username=name6
#userid=7, username=name7
#userid=8, username=name8
#userid=9, username=name9
