#! /usr/bin/python
# -*- coding: UTF-8 -*-
import re,urllib,urllib2
import os,sys,time
#import binascii

url_link = 'http://g.e-hentai.org/s/deba1aaf1f/341392-1'

def downJPG(link,num):
    jpg_file = '/%d.jpg' % num
    print "print download jpg url %s to file %s" %(link,jpg_file)
    data = urllib.urlretrieve(link,jpg_file)
    print "download ok!"
# print len(data)
# f = file(jpg_file,'wb')
# f.write(data)
# f.close()


def findLink(link,num):
    if num > 18:sys.exit(0)
    respone = urllib2.urlopen(link)
    text = respone.read()
    respone.close()
    down_link = re.compile(r'http:\/\/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{1,5}\/h\/.*\/keystamp\=[0-9]{1,}-.[0-9a-zA-Z]{,20}/[0-9a-zA-Z]{1,6}\.jpg').findall(text)
    if len(down_link)>0:
        downJPG(down_link[0],num)
    next_link = re.compile(r'<\/iframe><a href\="http:\/\/g.e-hentai.org\/s\/[0-9a-zA-Z]{,15}\/[0-9]{,10}\-[0-9]{,4}').findall(text)[0][18:]
    findLink(next_link,num+1)


if __name__ == '__main__':
    findLink(url_link,1)
