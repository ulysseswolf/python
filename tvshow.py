#!/usr/bin/python
# coding=UTF-8 
import os
import sys
import MySQLdb
import datetime
import time
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import codecs

#print sys.getdefaultencoding()

reload(sys)
sys.setdefaultencoding('utf-8')

d=datetime.datetime.now()
#Monday is 1
day=d.weekday()+1
today = datetime.date.today()
logName = '/root/tvlist_py/tv-%s.log' % today
logfile = codecs.open(logName,'a',encoding='utf-8')

taskCount = 10  

def openDB():
    return MySQLdb.connect(host="10.99.63.165", port=3306, user="root", passwd="", db="test", charset='utf8')
    #return MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="root", db="tv", charset='utf8')

def Log(str):
    logfile.write(str + '\n')
   
def visitAndParse(channels):
    conn = openDB()
    c=conn.cursor()
    for i in channels:
        for j in range(1-day,8-day):
        #for j in range(1-day,2-day):
            try:
                dayparam=today+datetime.timedelta(days=j)
                urlstr="http://v.163.com/tvlist/getSingleMessage2.jsp?tid=%d&time=%s" % (i[0],dayparam)
                Log('parsing %s ...' % urlstr)
                response = urllib2.urlopen(url=urlstr)
                html=response.read().decode('gbk','ignore')
                #if str(dayparam) == '2012-05-14':
                    #Log(html)
                #print html
            except urllib2.HTTPError, e:
                print e.code
            except Exception, e:
                print e

            soup=BeautifulSoup(html)
            nodelist = soup('span',attrs={"class" : re.compile("^t")})
            if len(nodelist) == 0:
                Log('0 records')
            for oneshow in nodelist:
                contents = []
                if oneshow['class']=='time':
                    shorttime=oneshow.string
                    beginTime=str(dayparam)+" "+shorttime+":00"
                if oneshow['class']=='til':
                    title=oneshow.string
                    #Log("%d,%s,%s" % (i[0],beginTime,title))
                    createTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    t = (i[0],beginTime,title,createTime)
                    contents.append(t)

                T = tuple(contents)
                c.executemany('INSERT INTO CONTENT_PROGRAM (CHANNEL_ID,BEGIN_TIME,TITLE,DURATION,CREATE_TIME) VALUES(%s,%s,%s,0,%s) ON DUPLICATE KEY UPDATE PROGRAM_ID = PROGRAM_ID',T)
                #for t in T:
                    #Log('INSERT INTO CONTENT_PROGRAM (CHANNEL_ID,BEGIN_TIME,TITLE,DURATION,CREATE_TIME) VALUES(%s,%s,%s,0,%s) ON DUPLICATE KEY UPDATE PROGRAM_ID = PROGRAM_ID' % t)
                
        conn.commit()
    c.close()
    conn.close()
                    
def update():
    conn = openDB()
    c=conn.cursor()

    starttime=str(today-datetime.timedelta(days=day-1))+" 00:00:00"
    endtime=str(today+datetime.timedelta(days=7-day))+" 23:59:59"

    Log("update data from %s to %s..." % (starttime,endtime))

    c.execute("update CONTENT_PROGRAM as T1 inner join  (select PROGRAM_ID, case when @lasttime='' or @lastcid <> CHANNEL_ID then 0 else UNIX_TIMESTAMP(@lasttime) -  UNIX_TIMESTAMP(BEGIN_TIME) end as DURATION,(@lasttime:=BEGIN_TIME),(@lastcid:=CHANNEL_ID) from CONTENT_PROGRAM,(select @lasttime:='', @lastcid:='') as t WHERE BEGIN_TIME >= %s AND BEGIN_TIME <= %s ORDER BY CHANNEL_ID,BEGIN_TIME DESC) as T2 on T1.PROGRAM_ID = T2.PROGRAM_ID set T1.DURATION = T2.DURATION",(starttime,endtime))
    conn.commit()
    c.close()
    conn.close()

def task(index):
    conn = openDB()
    cursor=conn.cursor()
    count=cursor.execute("SELECT CHANNEL_ID FROM CHANNEL_INFO")
    channelsPerTask = count / taskCount
    fromId = channelsPerTask * index
    SQL_SELECT_CHANNELS = u"SELECT CHANNEL_ID FROM CHANNEL_INFO LIMIT %s,%s"
    limit = channelsPerTask
    if index + 1 == 10:
        limit = channelsPerTask + 1
    cursor.execute(SQL_SELECT_CHANNELS,(fromId,limit))
    Log(SQL_SELECT_CHANNELS %(fromId,limit))
    channels = cursor.fetchall()
    visitAndParse(channels)
    
    cursor.close()
    conn.close() 
    
def main():
    startTime = time.time()
    tasks = []
    childPid = 0
    
    for i in range(taskCount):
        childPid = os.fork()
        if childPid == 0:          
            task(i)
            break
        else:
            tasks.append(childPid)

    if childPid != 0:
        while len(tasks) > 0:
            (pid,code) = os.wait()
            Log('[pid %d] task finished' % pid)
            tasks.remove(pid)
          
        update()
        endTime = time.time()
        Log('total time:%d' % int(endTime-startTime))
        Log("mission complete!")
            
        logfile.close()

def test():
    startTime = time.time()
    conn = openDB()
    cursor=conn.cursor()    
    count=cursor.execute("SELECT CHANNEL_ID FROM CHANNEL_INFO")
    channels = cursor.fetchall()           
    visitAndParse(channels) 
    cursor.close()
    update()
    conn.close()
    endTime = time.time()
    Log('total time:%d' % int(endTime-startTime))
    Log('mission complete!')
    logfile.close()


#test() 
main()


