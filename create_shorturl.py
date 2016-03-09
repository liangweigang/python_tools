#coding:utf-8
#Auth:liangweigang@outlook.com
#功能生成短链接
#注里是单线程跑的。若确实量大的话，可以使用多线程

import urllib
import urllib2
import re

def getShortUrl(szSourceURL):
    szUrl = 'http://www.waqiang.com/index.php/url/shorten'
    Values = { 'url': szSourceURL}
    RequestData = urllib.urlencode(Values)
    Request = urllib2.Request(szUrl, RequestData)
    Response = urllib2.urlopen(Request)
    szPageText = Response.read()
    szPageText = szPageText.replace('\r','').replace('\n','')#.find()
    FindList = re.findall('<input name="url" id="url".*?\/>',szPageText,re.I)
    if len(FindList) == 0:
        print 'the tools does not work, please update it.'
    szRetUrl = FindList[0][80:-4]
    return szRetUrl
  
#szFile:        要传换的文件
#szResultFile:  结果文件
#nColumnNum:    转换在第几列(从0开始)
#szSep:         列分隔符
def ConverFile(szFile, szResultFile, nColumnNum, szSep='|,|'):
    File1 = open(szFile, 'r')
    File2 = open(szResultFile, 'w')
    for szLine in File1:
        szFile = szFile.replace('\r', '').replace('\n', '')
        Item = szLine.split(szSep)
        szShort = getShortUrl(Item[nColumnNum])
        print szFile
        n = 0
        while n < nColumnNum:
            File2.write(Item[n])
            File2.write(szSep)
            n = n + 1
        File2.write(szShort)
        File2.write(szSep)
        n = nColumnNum

        while n < len(Item):
            File2.write(szShort)
            File2.write(szSep)
            n = n + 1
    File1.close()
    File2.close()

if __name__ == '__main__':
    #szSourceFile = sys.argv[1]
    #szResultFile = sys.argv[2]
    #nColumnNum   = sys.argv[3]
    #szSep        = sys.argv[4]
    szSourceFile = 'e:/aa.txt'
    szResultFile = 'e:/bb.txt'
    nColumnNum   = 1
    szSep        = '|,|'

    ConverFile(szSourceFile, szResultFile, nColumnNum, szSep)
    #print getShortUrl('http://baidu.com')
    #test Example:
    #ConverFile('e:/aaa.txt', 'e:/bb.txt', 1, '|,|')