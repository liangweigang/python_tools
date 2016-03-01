#! -*- coding:utf-8 -*-
import json
import re
import urllib2
import time
import os
import sys
import datetime
import codecs

#已经废弃
def getContentOfSingleTiezi():
    #tid = 2378003356
    url = 'http://trading.5173.com/list/viewlastestdeallist.aspx?gm=a36ead01453c40b584f8e1e687723f2d&bt=682b60e289f045339cae13d208023fc6&pg=1&ps=4000'
    page_data = urllib2.urlopen(url).read()#.decode('gbk', 'ignore')  
    page_data = page_data.replace('\r\n','')#.replace('','')
    find_list1 = re.findall('<div class="listmain .*?<\/div>', page_data, re.I)
    
    f=open('E:\\daily-work\\jx35173\\aaa.txt','w')
    for list in find_list1:
        sublist = re.findall('<li.*?<\/li>', list, re.I)
        #print len(sublist)
        
        for i in range(len(sublist)):
            li = sublist[i]
            if i == 0:
                it = datetime.date.today().strftime('%Y%m%d')
            elif i == 1:
                li = li.replace('<li>','')
                li = li.replace('</li>','')
                li = li.replace('游戏/区/服/阵营：剑侠情缘Ⅲ/','')
                it =li
            elif i == 3:
                li = li.replace('<li class="orange">','')
                li = li.replace('</li>','')
                li = li.replace('元','')
                li = li.replace(',','')
                it = li
            elif (i == 4) and len(sublist)==7:
                li = li.replace('元/通宝','')
                a = li.find('orange">')+8
                b = li.find('</span')
                it = li[a:b].replace('元/金','').replace('元/通宝','')
            elif (i==5) and len(sublist)==6:
                li = li.replace('<li class="in_ac">','')
                li = li.replace('</li>','')
                it = '|,|' + li
            elif (i == 6) and len(sublist)==7:
                li = li.replace('<li class="in_ac">','')
                li = li.replace('</li>','')
                it = li
            else:
                continue
            f.write(it)
            f.write('|,|')
        f.write('\n')
    f.close()
    


#deg startDayStr =< dill_time  < endDayStr
def getContentOfSingleDay(startDayStr,endDayStr):
    url = 'http://trading.5173.com/list/viewlastestdeallist.aspx?gm=a36ead01453c40b584f8e1e687723f2d&bt=682b60e289f045339cae13d208023fc6&pg=1&ps=4000'
    page_data = urllib2.urlopen(url).read()#.decode('gbk', 'ignore')  
    page_data = page_data.replace('\r\n','')#.replace('','')
    find_list1 = re.findall('<div class="listmain .*?<\/div>', page_data, re.I)
    
    f=open('E:\\daily-work\\jx35173\\'+startDayStr+'.txt','w')
    for list in find_list1:
        sublist = re.findall('<li.*?<\/li>', list, re.I)
        
        dill_time = sublist[6]
        dill_time = dill_time.replace('<li class="in_ac">','')
        dill_time = dill_time.replace('</li>','')
        
        if not(dill_time >= startDayStr and dill_time < endDayStr):
            continue
        
        game_server = sublist[1]
        game_server = game_server.replace('<li>','')
        game_server = game_server.replace('</li>','')
        game_server = game_server.replace('游戏/区/服/阵营：剑侠情缘Ⅲ/','')
        a = game_server.find('区/') + 2
        server1 = game_server[0:a]
      
        server2 = game_server.replace(server1,'')[1:]
        b = server2.find('/')
        if b == -1:
            server2 = server2
        else:
            server2 = server2[0:b]
        
        price = sublist[3]
        price = price.replace('<li class="orange">','')
        price = price.replace('</li>','')
        price = price.replace('元','')
        price = price.replace(',','')
        
        
        unit_price = sublist[4]
        unit_price = unit_price.replace('元/通宝','').replace('元/金','')
        a = unit_price.find('orange">')+8
        b = unit_price.find('</span')
        unit_price = unit_price[a:b]
        
        
        f.write(startDayStr)
        f.write('|,|')
        f.write(server1)
        f.write('|,|')
        f.write(server2)
        f.write('|,|')
        f.write(price)
        f.write('|,|')
        f.write(unit_price)
        f.write('|,|')
        f.write(dill_time)
        f.write('|,|')
        f.write('\n')

    f.close()

#dateStr=sys.argv[1]

dateStr = '30130820'
adate = datetime.datetime.strptime(dateStr, '%Y%m%d')
bdate = adate + datetime.timedelta(days=1)
startDayStr = adate.strftime('%Y-%m-%d')
endDayStr = bdate.strftime('%Y-%m-%d')


print startDayStr
print endDayStr
 

getContentOfSingleDay('2013-08-20','2013-08-21')