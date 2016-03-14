#coding:utf-8
#/usr/bin/python
#auth:liangweigang@outlook.com

#just list few useage more visit:https://pypi.python.org/pypi/redis

import redis

class RedisHelper:
    def __init__(self, szHost, szPort, szPasswd, szDBNUM):
        self.m_Redis = None
        try:
            self.m_Redis = redis.StrictRedis(host=szHost, port=szNWRedisPort, password=szPasswd, db=szDBNUM)
        except Exception, e:
            print str(e)
            raise e

    def __del__(self):
        #connection is auto closed 
        pass
        #if self.m_Conn is not None:
        #    self.m_Conn.close()

    def Hset(self, szParentKey, szSUbKey, szContent):
        try:
           self.m_Redis.hset(szParentKey, szSUbKey, szContent)
        except Exception, e:
            print str(e)
            raise e

    #### for example: hest infa a1 1  a2 4 a3 3
    #### we can use:
    # Dict = {}
    # Dict['a1'] = 1
    # Dict['a2'] = 2
    # Dict['a3'] = 3
    # HSETWithDict('infa', Dict)
    def HsetWithDict(self, szParentKey, SubKeyDict):
        try:
           self.m_Redis.hset(szParentKey, SubKeyDict)
        except Exception, e:
            print str(e)
            raise e

    def PipelineExample(self):
        Pipe = self._redis.pipeline(transaction=False);
        Pipe.set('infa:11', '1')
        Pipe.set('infa:12', '2')
        Pipe.execute()

# del all redis key with shell command
# redis-cli  keys "infa:*" | xargs redis-cli del
# redis-cli -a passwd keys "infa:*" | xargs -L1 -I '$' echo '"$"' | xargs redis-cli -a passwd del

