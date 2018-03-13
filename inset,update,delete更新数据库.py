#inset,update,delete更新数据库
#开始-->创建connection-->获取cursor-->使用cursor.execute()执行i/u/d语句
#-->出现异常-->是/否-->使用conn.commit()提交事务/使用conn.rollback()回滚事务-->关闭cursor-->关闭connection-->结束

#事务:访问和更新数据库的一个程序执行单元
#原子性: 事务中包括的诸操作要么都做，要么都不做
#一致性: 事务必须使数据库从一致性状态变到另一个一致性状态
#隔离性: 一个事务的执行不能被其他事务干扰
#持久性: 事务一旦提交，它对数据库的改变就是永久性的

#开发中怎样使用事务?
#关闭自动commit: 设置conn.autocommit(False)
#正常结束事务: conn.commit()
#异常结束事务: conn.rollback()



#数据库
userid  username
1       name1
2       name2
3       name3
4       name4
5       name5
6       name6
7       name7
8       name8
9       name9

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
print(conn)
print(cursor)

sql_insert = "insert into user(userid, username) values(10, 'name10')"
sql_update = "update user set username='name91' where userid=9"
sql_delete = "delete from user where userid<3"

cursor.execute(sql_insert)
print(cursor.rowcount)  #1
cursor.execute(sql_update)
print(cursor.rowcount)  #1
cursor.execute(sql_delete)
print(cursor.rowcount)  #2
#此时数据库未改变
conn.commit()  #数据库改变

cursor.close()
conn.close()

#数据库变为：
userid  username
3       name3
4       name4
5       name5
6       name6
7       name7
8       name8
9       name91
10      name10



#测试conn.rollback()
#数据库
userid  username
1       name1
2       name2
3       name3
4       name4
5       name5
6       name6
7       name7
8       name8
9       name9

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
print(conn)  #<pymysql.connections.Connection object at 0x00000219B71FC048>
print(cursor)  #<pymysql.cursors.Cursor object at 0x00000219B7BC7C50>

sql_insert = "insert into user(userid, username) values(10, 'name10')"
sql_update = "update user set username='name91' where userid=9"
sql_delete = "delete from user where userd<3"  #useid-->usrd

try:
    cursor.execute(sql_insert)
    print(cursor.rowcount)  #1
    cursor.execute(sql_update)
    print(cursor.rowcount)  #1
    cursor.execute(sql_delete)  #跳到异常
    print(cursor.rowcount)
    
    conn.commit()
except Exception as e :
    print(e)  #(1054, "Unknown column 'userd' in 'where clause'")
    conn.rollback()

cursor.close()
conn.close()

#数据库不变，回滚（conn.rollback()）起作用
