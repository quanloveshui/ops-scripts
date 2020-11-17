#!/usr/bin/python2.6
# -*- coding: UTF-8 -*-


#python操作oracle

import cx_Oracle

select = "select assetid,fileurl from T_VIDEO_ITEM where assetid in "
file = open('ystenid')
line = file.readlines()
file.close()
listid = []
for i in line:
    i = i.strip('\n')
    listid.append(i)
#print listid
conn = cx_Oracle.connect('xxxx/xxx@x.x.x.x.:1521/media')
cursor = conn.cursor ()
sql = select + str(tuple(listid))
print sql
cursor.execute (sql)
rows = cursor.fetchall()
#print rows
for i in rows:
    id = i[0]
    url = i[1]
    #print id,url
    file = open('url','a+')
    file.write(id + ' ')
    file.write(url + '\n')
    file.close()
