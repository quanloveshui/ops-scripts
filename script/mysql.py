#!/usr/bin/env python

#python操作mysql

import MySQLdb,os,sys

dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir)

from config import myconf

def select(name):
    db=MySQLdb.connect(host=myconf.host,port=myconf.port,user=myconf.user,passwd=myconf.passwd,db=myconf.db)
    cursor = db.cursor()
    sql="select Name,Password from user where Name='%s'" % name
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    #print data
    #while data:
    return data

def insert(name,passwd):
    db=MySQLdb.connect(host=myconf.host,port=myconf.port,user=myconf.user,passwd=myconf.passwd,db=myconf.db)
    cursor = db.cursor()
    sql="insert into user (Name,Password) values ('%s','%s')" % (name,passwd)
    flag=""
    try:
        cursor.execute(sql)
        db.commit()
        print "insert into is sucess"
        flag="True"
    except:
        print "insert into is failure"
        db.rollback()
    db.close()
    return flag
