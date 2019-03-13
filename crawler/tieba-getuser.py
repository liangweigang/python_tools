#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Auth: liangweigang
# 目的: 从贴吧取数据时，瓶颈卡在网络IO上，
#       建了一个线程池的通用库，以后跑贴吧数据可以直接调用
#       下面的示例是取所以关注放开那三国的人的示例
import Queue
import threading
import time
import json
import re
import urllib2,urllib
import time
import os
import sys
import datetime
import codecs
import argparse



class KThread (threading.Thread):
    def __init__(self, nThreadID, ThreadFunc):
        threading.Thread.__init__(self)
        self.m_nThreadID    = nThreadID
        self.m_ThreadFunc   = ThreadFunc

    def run(self):
        print "Starting " , self.m_nThreadID , '\n'
        self.m_ThreadFunc(self.m_nThreadID)
        print "Exiting " , self.m_nThreadID, '\n'

'''
nPoolsize: 　启动线程个数
ltTaskList：要处理的任务列表

cbTaskFunc: 
参数: ltTaskList中的单个元素
返回: list 
注意: 被多个线程调用，注意线程安全

cbResultFunc:
参数:Item 返回list中的单个元素
返回: 无

注意:只在主线程中调用
'''
class KThreadPool:
    def __init__(self, nPoolsize, ltTaskList, cbTaskFunc, cbResultFunc):
        self.m_nPoolsize    = nPoolsize
        self.m_cbTaskFunc   = cbTaskFunc
        self.m_cbResultFunc = cbResultFunc

        self.m_TaskMutex    = threading.Lock()
        self.m_TaskQueue    = Queue.Queue(1000000)

        self.m_ResultQueue  = Queue.Queue(100000)
        self.m_ResultMutex  = threading.Lock()
        self.m_ltThread     = []
        self.m_bRunFlag     = True
        self.m_nTaskCount   = 0

        for Item in ltTaskList:
            self.m_TaskQueue.put(Item)

        for i in range(nPoolsize):
            nThreadID = i
            thread = KThread(nThreadID, self.ThreadFunc)
            self.m_ltThread.append(thread)

    def Start(self):
        for Thread in self.m_ltThread:
            Thread.start()

    def InitTaskQueue(self, ltTaskList):
        print 'Init success.'
        if len(ltTaskList) <= 0:
            return
        self.m_TaskMutex.acquire()
        for Item in ltTaskList:
            self.m_TaskQueue.put(Item)
        self.m_TaskMutex.release()
        print 'Init Task success'

    #main thread
    def Run(self):
        for Thread in self.m_ltThread:
            Thread.start()

        #等待队列清空
        while not self.m_TaskQueue.empty():
            if not self.m_ResultQueue.empty():
                self.m_ResultMutex.acquire()
                while not self.m_ResultQueue.empty():
                    Item = self.m_ResultQueue.get()
                    self.m_cbResultFunc(Item)
                self.m_ResultMutex.release()
        self.m_bRunFlag = False

        #等待所有线程退出
        for Thread in self.m_ltThread:
            Thread.join()

        #再检查一下结果队列,可能了线程退出时又产生的结果。
        while not self.m_ResultQueue.empty():
            Item = self.m_ResultQueue.get()
            self.m_cbResultFunc(Item)
        print "Exiting Main Thread"
        
    def ThreadFunc(self, nThreadID):
        while self.m_bRunFlag:
            Item = None

            self.m_TaskMutex.acquire()
            if not self.m_TaskQueue.empty():
                Item = self.m_TaskQueue.get()
                self.m_nTaskCount += 1
                print "Have complete (%d) tasks.\n" % self.m_nTaskCount
            self.m_TaskMutex.release()
            
            if Item is None:
                continue

            ResultArray = self.m_cbTaskFunc(Item)
            if ResultArray and  len(ResultArray) > 0:
                self.m_ResultMutex.acquire()
                for Item in ResultArray:
                    self.m_ResultQueue.put(Item)
                self.m_ResultMutex.release()


########################################################################
#下面是一个应用示例
########################################################################

#任务处理回调函数
#获取一个排行榜页面下的人的信息
def GetUsersSinglePage(szURL):
    while 1:
        try:
            req = urllib2.Request(szURL)
            szPageData = urllib2.urlopen(szURL).read()
            break;
        except Exception, e:
            print e
            time.sleep(0.5)
            continue
    find_list1 = re.findall('<tr class="drl_list_item".*?<\/tr>', szPageData, re.I)
    ltRet = []
    for Record in find_list1:
        szRank = re.findall('<p class="drl_.*?<\/p>', Record)[0]
        nFindPos = szRank.find('>')
        szRank = szRank[nFindPos + 1 : -4]

##        szLevel  = re.findall('div class="bg_.*?">', Record)[0]
##        nFindPos = szLevel.find('lv')
##        szLevel  = szLevel[nFindPos + 2 : -2]

        szName   = re.findall('username.*?\/a>', Record)[0]
        nFindPos = szName.find('>')
        szName   = szName[nFindPos + 1 : -4]

        szExperience = re.findall('drl_item_exp.*?\/span>', Record)[0]
        nFindPos     = szExperience.find('span')
        szExperience = szExperience[nFindPos + 5 : -7]

##        szHomeURL = re.findall('<div class="drl_item_card.*?target', Record)[0]
##        nFindPos  = szHomeURL.find('href="')
##        szHomeURL = szHomeURL[nFindPos + 6 : -8]
##        szWriteLine = ("%s|,|%s|,|%s|,|%s|,|%s") %(szRank, szName, szLevel, szExperience, szHomeURL)
        szName = str(szName).decode('gbk').encode('utf-8')
        szWriteLine = ("%s|,|%s|,|%s") %(szRank, szName, szExperience)

        ltRet.append(szWriteLine)
    return ltRet

#任务结果回调函数
def WriteResult(Item):
    global g_ResultFile
    g_ResultFile.write(Item + '\n')

#获取一个排行榜页面下的本吧会员数
def GetUsersCount(szURL):
    while 1:
        try:
            req = urllib2.Request(szURL)
            szPageData = urllib2.urlopen(szURL).read()
            break;
        except Exception, e:
            print e
            time.sleep(0.5)
            continue
    szCount   = re.findall('drl_info_txt_gray.*?\/span>', szPageData)[0]
    nFindPos = szCount.find('>')
    szCount   = szCount[nFindPos + 1 : -7]
    if szCount.isdigit():
        return int(szCount)
    else:
        return -1

def Run(szTiebaName, szResultFilePath):
    global g_ResultFile;
    g_ResultFile = codecs.open(szResultFilePath, "w")

    ltTask = []
    #贴吧排行榜地址
    szPrefix  = "http://tieba.baidu.com/f/like/furank?kw="
    szPostfix = "&pn="

    szURLPrefix="%s%s%s" % (szPrefix, urllib.quote(szTiebaName), szPostfix)
    nPage = 1
    nTotalUser = GetUsersCount(szURLPrefix)
    #创建任务列表
    while nPage < nTotalUser / 20 + 1:
        szPageURL = szURLPrefix + str(nPage)
        ltTask.append(szPageURL)
        nPage = nPage + 1

    Pool = KThreadPool(20, ltTask, GetUsersSinglePage, WriteResult)
    Pool.Run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str, required=True, help="Name of tieba.")
    parser.add_argument('-f', '--file', type=str, required=True, help="result file path.")
    Args = parser.parse_args()
    szTiebaName      = Args.name
    szResultFilePath = Args.file

    Run(szTiebaName, szResultFilePath)

