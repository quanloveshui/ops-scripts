#!/usr/bin/python2.6
# -*- coding: UTF-8 -*- 

#python操作oracle

import urllib
import urllib2
import cx_Oracle
import time
import datetime

def conndb(username,passwd,ip,sid):
    conn = username + '/' + passwd + '@' + ip + '/' + sid
    db = cx_Oracle.connect(conn)
    return db

def Selectdb(db,sql):
    cursor = db.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    return result


print 'connect databases'
db=conndb('xxxx','xxxx','xxxx:1521','sjh')
sql = "select  ''|| cpr.contentId ||'|'||ps.productId ||'' from SCSP_CONTENT_PRODUCT_RELATION cpr,SCSP_PRODUCT_STRATEGY ps where ps.code=cpr.strategy_Code"
rs = Selectdb(db,sql)
for i in rs:
    print i[0].strip()


