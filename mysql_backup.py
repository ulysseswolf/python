#!/usr/bin/python3
#coding=utf-8

import pymysql
import csv
import codecs
import chardet
import sys
import os,datetime
import time
import string
import pytz
import copy
import importlib
import re
import time
import logging

import imaplib
import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import COMMASPACE,formatdate
from email import encoders

import subprocess

## connect to MySQL

## comment variables ##########################################
## time zone
utc = pytz.utc
tz = pytz.timezone('Asia/Shanghai')
d=datetime.datetime.now(tz)
mysql_host = 'ud094661c879c59fa6e9e'
mysql_user = 'tam'
mysql_password = 'kindle'
mysql_default_db = 'tam_db'
work_path = '/home/tam/deploy'
## mysql configuration
importlib.reload(sys)

##logging configuration
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)3d] %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %a %H:%M:%S',
                filename=work_path+'/MysqlBackup.log',
                filemode='w')
months = {'jan':'01','feb':'02','mar':'03','apr':'04','may':'05','jun':'06','jul':'07','aug':'08','sep':'09','oct':'10','nov':'11','dec':'12'}

#reminder mail address
reminder_mail_address = "yongqis@amazon.com"
#batchsize for loading
batchsize = 10000
###############################################################
backup_dir = '/mnt/wind/YQ/mysql_daily_backup'

logging.info('connecting to DB server - ' + mysql_host)
conn=pymysql.connect(host= mysql_host,user= mysql_user,passwd= mysql_password,db= mysql_default_db,port=3306,local_infile=1,charset='utf8',cursorclass=pymysql.cursors.DictCursor)
cursor=conn.cursor()
logging.info('connected  to DB server - ' + mysql_host)

cur_day = str(datetime.datetime.now().date())
if os.path.exists(backup_dir+os.sep+cur_day):
    os.system("rm -rf "+backup_dir+os.sep+cur_day+os.sep+"*.sql")
else:
    os.system("mkdir -p "+backup_dir+os.sep+cur_day)
cursor.execute("select schema_name from information_schema.SCHEMATA where SCHEMA_NAME not in ( 'information_schema','mysql','performance_schema','sys' )")
for database in cursor.fetchall():
    backup_file = backup_dir+os.sep+cur_day+os.sep+database['schema_name']+".sql"
    cmd = "mysqldump -utam -pkindle  %s > %s" % ( database['schema_name'], backup_file )
    os.system(cmd)
#cleanup the older dirs
for dd in os.listdir(backup_dir):
    temp = re.findall(r'^(\d{4})-(\d{1,2})-(\d{1,2})$', dd)
    if len(temp) < 1: continue
    age = (datetime.datetime.strptime(cur_day, '%Y-%m-%d').date() - datetime.datetime.strptime(dd, '%Y-%m-%d').date()).days
    if age>7:
        try:
            os.system("rm -rf " + backup_dir + os.sep + dd + os.sep+"*")
            os.system("rmdir " + backup_dir + os.sep + dd )
        except Exception as e:
            logging,info("failed with exception of "+repr(e)+" on " +dd)
        logging.info('cleanup the dir of ' + dd)
