#coding:utf-8
#/usr/bin/python
#auth:liangweigang@outlook.com
import cx_Oracle

class OracleHelper:
    def __init__(self, szUser, szPasswd, szOraSID):
        self.m_Conn = None
        try:
            szConnstr = '%s/%s@%s'%(szUser, szPasswd, szOraSID)
            self.m_Conn = cx_Oracle.connect(szConnstr)
        except Exception, e:
            print str(e)
            raise e

    def __del__(self):
        if self.m_Conn is not None:
            self.m_Conn.close()

    def Select(self, szSql):
        try:
            Cursor = self.m_Conn.cursor()
            Cursor.execute(szSql)
            results = Cursor.fetchall()
            Cursor.close()
            return results
        except Exception, e:
            print str(e)
            raise e

    def DML(self, szSql):
        try:
            Cursor = self.m_Conn.cursor()
            Cursor.execute(szSql)
            self.m_Conn.commit()
            Cursor.close()
        except Exception, e:
            print str(e)
            raise e

'''
#### use-case:
szUser      = 'root'
szPasswd    = 'admin'
szSID       = 'ora_test'

#connect
ORACLE = OracleHelper(szUser, szPasswd, szSID)

#####---select---###########
Result = ORACLE.Select("select * from test")
for Item in Result:
    print Item
#####---insert---###########
szSQL = "insert into test values(15, 'test')"
ORACLE.DML(szSQL)
'''
