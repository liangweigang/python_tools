#coding:utf-8
#/usr/bin/python
#auth:liangweigang@outlook.com
import MySQLdb

class MySQLHelper(object):
    def __init__(self, szHost, nPort, szUser, szPasswd, szDBName, szCharSet='gbk'):
        self.m_Conn = None
        try:
            self.m_Conn = MySQLdb.connect(  \
                host = szHost               \
                ,port = nPort               \
                ,user = szUser              \
                ,passwd = szPasswd          \
                ,db = szDBName              \
                ,charset = szCharSet)
        except Exception, e:
            print str(e)
            raise e

    def __del__(self):
        if self.m_Conn is not None:
            self.m_Conn.close()

    def Select(self, szSQL):
        try:
            Cursor = self.m_Conn.cursor()
            Cursor.execute(szSQL)
            Result = Cursor.fetchall()
            Cursor.close()
            return Result
        except Exception, e:
            print str(e)
            raise e

    def DML(self, szSQL):
        try:
            Cursor = self.m_Conn.cursor()
            Cursor.execute(szSQL)
            self.m_Conn.commit()
            Cursor.close()
        except MySQLdb.Warning:
            #not process mysql warning.
            return
        except Exception, e:
            print str(e)
            raise e


#### use-case:
szHost      = '127.0.0.1'
szPort      = '3306'
szUser      = 'root'
szPasswd    = 'admin'
szDBName    = 'test'
szCharSet   = 'gbk'

#connect
MYSQL = MySQLHelper(szHost, int(szPort), szUser, szPasswd, szDBName, szCharSet)

#####---select---###########
Result = MYSQL.Select("select * from test")
for Item in Result:
    print Item
#####---insert---###########
szSQL = "insert into test values(15, 'test')"
MYSQL.DML(szSQL)

