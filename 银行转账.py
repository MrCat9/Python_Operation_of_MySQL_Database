#开始事务-->检查账户A和账户B是否可用-->检查账户A是否有100元-->账户A减去100元，账户B加上100元-->提交事务
#-->出现异常-->回滚事务

#创建数据库
CREATE TABLE account (
  acctid INT(11) DEFAULT NULL COMMENT '账户ID',
  money INT(11) DEFAULT NULL COMMENT '余额'
) ENGINE = INNODB DEFAULT CHARSET = utf8

-- 因为转账操作需要事务的支持，所以引擎不能用MyISAM，要用INNODB才能回滚

#数据库
acctid    money
11        110
12        10

#
#coding:utf8  #设置编码
import sys
import pymysql

class TransferMoney(object):
    def __init__(self, conn):
        self.conn = conn
    
    def check_acct_available(self, acctid):
        cursor = self.conn.cursor()
        try:
            sql = 'select * from account where acctid=%s'%acctid
            cursor.execute(sql)
            print('check_acct_available:'+sql)
            rs = cursor.fetchall()
            if len(rs)!=1:
                raise Exception('no account id:%s'%acctid)
        finally:
            cursor.close()
    
    def has_enough_money(self, acctid, money):
        cursor = self.conn.cursor()
        try:
            sql = 'select * from account where acctid=%s and money>%s'%(acctid, money)
            cursor.execute(sql)
            print('has_enough_money:'+sql)
            rs = cursor.fetchall()
            if len(rs)!=1:
                raise Exception('account %s has no enough money'%acctid)
        finally:
            cursor.close()   
    
    def reduce_money(self, acctid, money):
        cursor = self.conn.cursor()
        try:
            sql = 'update account set money=money-%s where acctid=%s'%(money, acctid)
            cursor.execute(sql)
            print('reduce_money:'+sql)
            if cursor.rowcount!=1:
                raise Exception('account %s reduce money fail'%acctid)
        finally:
            cursor.close()
   
    def add_money(self, acctid, money):
        cursor = self.conn.cursor()
        try:
            sql = 'update account set money=money+%s where acctid=%s'%(money, acctid)
            cursor.execute(sql)
            print('add money:'+sql)
            if cursor.rowcount!=1:
                raise Exception('account %s add money fail'%acctid)
        finally:
            cursor.close()
        
    def transfer(self, source_acctid,target_acctid,money):
        try:
            self.check_acct_available(source_acctid)
            self.check_acct_available(target_acctid)
            self.has_enough_money(source_acctid, money)
            self.reduce_money(source_acctid, money)
            self.add_money(target_acctid, money)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e 

if __name__=="__main__":
    source_acctid = sys.argv[1]
    target_acctid = sys.argv[2]
    money = sys.argv[3]
    
    conn = pymysql.Connect(host='127.0.0.1', user='root', passwd='123456', port=3306, db='pymysql_test01')
    tr_money = TransferMoney(conn)
    
    try:
        tr_money.transfer(source_acctid,target_acctid,money)
    except Exception as e:
        print("error:"+str(e))
    finally:
        conn.close()    

#Run Configuration --> 传入3个参数（source_acctid，target_acctid，money）  11 12 100
#console
#check_acct_available:select * from account where acctid=11
#check_acct_available:select * from account where acctid=12
#has_enough_money:select * from account where acctid=11 and money>100
#reduce_money:update account set money=money-100 where acctid=11
#add money:update account set money=money+100 where acctid=12

#数据库变化：
acctid    money
11        10
12        110



#账号B不存在，并且注释掉self.check_acct_available(target_acctid)，测试rollback()

#数据库
acctid    money
11        110
13        10

#
#coding:utf8
import sys
import pymysql

class TransferMoney(object):
    def __init__(self, conn):
        self.conn = conn
    

    def check_acct_available(self, acctid):
        cursor = self.conn.cursor()
        try:
            sql = 'select * from account where acctid=%s'%acctid
            cursor.execute(sql)
            print('check_acct_available:'+sql)
            rs = cursor.fetchall()
            if len(rs)!=1:
                raise Exception('no account id:%s'%acctid)
        finally:
            cursor.close()
    
    def has_enough_money(self, acctid, money):
        cursor = self.conn.cursor()
        try:
            sql = 'select * from account where acctid=%s and money>%s'%(acctid, money)
            cursor.execute(sql)
            print('has_enough_money:'+sql)
            rs = cursor.fetchall()
            if len(rs)!=1:
                raise Exception('account %s has no enough money'%acctid)
        finally:
            cursor.close()
    
    
    def reduce_money(self, acctid, money):
        cursor = self.conn.cursor()
        try:
            sql = 'update account set money=money-%s where acctid=%s'%(money, acctid)
            cursor.execute(sql)
            print('reduce_money:'+sql)
            if cursor.rowcount!=1:
                raise Exception('account %s reduce money fail'%acctid)
        finally:
            cursor.close()
    
    
    def add_money(self, acctid, money):
        cursor = self.conn.cursor()
        try:
            sql = 'update account set money=money+%s where acctid=%s'%(money, acctid)
            cursor.execute(sql)
            print('add money:'+sql)
            if cursor.rowcount!=1:
                raise Exception('account %s add money fail'%acctid)
        finally:
            cursor.close()
    
    
    def transfer(self, source_acctid,target_acctid,money):
        try:
            self.check_acct_available(source_acctid)
            #self.check_acct_available(target_acctid)
            self.has_enough_money(source_acctid, money)
            self.reduce_money(source_acctid, money)
            self.add_money(target_acctid, money)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e 



if __name__=="__main__":
    source_acctid = sys.argv[1]
    target_acctid = sys.argv[2]
    money = sys.argv[3]
    
    conn = pymysql.Connect(host='127.0.0.1', user='root', passwd='123456', port=3306, db='pymysql_test01')
    tr_money = TransferMoney(conn)
    
    try:
        tr_money.transfer(source_acctid,target_acctid,money)
    except Exception as e:
        print("error:"+str(e))
    finally:
        conn.close()    

#Run Configuration --> 传入3个参数（source_acctid，target_acctid，money）  11 12 100
#console
#check_acct_available:select * from account where acctid=11
#has_enough_money:select * from account where acctid=11 and money>100
#reduce_money:update account set money=money-100 where acctid=11
#add money:update account set money=money+100 where acctid=12
#error:account 12 add money fail

#数据库不变，回滚事务成功
acctid    money
11        110
13        10
