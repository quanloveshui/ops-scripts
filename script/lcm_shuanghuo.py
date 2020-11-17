#上海移动lcm双活脚本


一、lcm-content-query

#!/usr/bin/python2.6
# -*- coding: UTF-8 -*- 


import urllib
import urllib2
import cx_Oracle
import time
import datetime

def migu(id):
    content = '''<?xml version="1.0" encoding="UTF-8"?>
    <message module="CDN" version="3.0">
    <header action="REQUEST" command="CONTENT_QUERY" component-id="UServerHawk_10.200.17.33" component-type="UCE" sequence="670736641"/>
    <body>
    <session id="123"/>
    <contents>
    <content channel-id=miguvod content-repository-id=migu_REP protocol=IPHONEHTTP request-uri="/25000/xxx.m3u8?channel-id=miguvod&amp;Contentid=xxxx&amp;stbId=12345678&amp;owsid=123&amp;test=123&amp;owport=3302" cur-serial-num="0" request-serial-num="0" business-type="5" insert-ad="0" play-list="0" access-mark="xxxx" start-offset="0" speed-back="0"/>
    </contents>
   </body>
   </message>'''
    newcontent = content.replace('xxxx',id)
    return newcontent

def  bst(id):
    content = '''<?xml version="1.0" encoding="UTF-8"?>
    <message module="CDN" version="3.0">
    <header action="REQUEST" command="CONTENT_QUERY" component-id="UServerHawk_10.200.17.33" component-type="UCE" sequence="670736641"/>
    <body>
    <session id="123"/>
    <contents>
    <content channel-id=bstvod content-repository-id=bstvod protocol=IPHONEHTTP request-uri="/25000/xxx.m3u8?channel-id=bstvod&amp;Contentid=xxxx&amp;stbId=12345678&amp;owsid=123&amp;test=123&amp;owport=3302" cur-serial-num="0" request-serial-num="0" business-type="5" insert-ad="0" play-list="0" access-mark="xxxx" start-offset="0" speed-back="0"/>
    </contents>
    </body>
    </message>'''
    newcontent = content.replace('xxxx',id)
    return newcontent

def ysten(id):
    content = '''<?xml version="1.0" encoding="UTF-8"?>
    <message module="CDN" version="3.0">
    <header action="REQUEST" command="CONTENT_QUERY" component-id="UServerHawk_10.200.17.33" component-type="UCE" sequence="670736641"/>
    <body>
    <session id="123"/>
    <contents>
    <content channel-id=ysten content-repository-id=ysten_REP protocol=HTTP request-uri="/25000/xxx.ts?channel-id=ysten&amp;Contentid=xxxx&amp;stbId=12345678&amp;owsid=123&amp;test=123&amp;owport=3301" cur-serial-num="0" request-serial-num="0" business-type="5" insert-ad="0" play-list="0" access-mark="xxxx" start-offset="0" speed-back="0"/>
    </contents>
    </body>
    </message>'''
    newcontent = content.replace('xxxx',id)
    return newcontent

def cmcc(id):
    content = '''<?xml version="1.0" encoding="UTF-8"?>
    <message module="CDN" version="3.0">
     <header action="REQUEST" command="CONTENT_QUERY" component-id="UServerHawk_10.200.17.33" component-type="UCE" sequence="670736641"/>
    <body>
    <session id="123"/>
    <contents>
    <content channel-id=cmcc content-repository-id=cmcc_REP protocol=HTTP request-uri="/25000/xxx.ts?channel-id=cmcc&amp;Contentid=xxxx&amp;stbId=12345678&amp;owsid=123&amp;test=123&amp;owport=3301" cur-serial-num="0" request-serial-num="0" business-type="5" insert-ad="0" play-list="0" access-mark="xxxx" start-offset="0" speed-back="0"/>
    </contents>
    </body>
    </message>'''
    newcontent = content.replace('xxxx',id)
    return newcontent

def test(id):
    content = '''<?xml version="1.0" encoding="UTF-8"?>
    <message module="CDN" version="3.0">
    <header action="REQUEST" command="CONTENT_QUERY" component-id="UServerHawk_10.200.17.33" component-type="UCE" sequence="670736641"/>
    <body>
    <session id="123"/>
    <contents>
    <content channel-id=test content-repository-id=test_REP protocol=HTTP request-uri="/25000/xxx.ts?channel-id=test&amp;Contentid=xxxx&amp;stbId=12345678&amp;owsid=123&amp;test=123&amp;owport=3301" cur-serial-num="0" request-serial-num="0" business-type="5" insert-ad="0" play-list="0" access-mark="xxxx" start-offset="0" speed-back="0"/>
    </contents>
    </body>
    </message>'''
    newcontent = content.replace('xxxx',id)
    return newcontent

def delete(id,REP):
    url = 'http://x.x.x.x:x'
    info = '''<?xml version="1.0" encoding="UTF-8"?>
<message module="CDN" version="3.0">
        <header action="REQUEST" command="CONTENT_INFO_QUERY" component-id="cnoss01" component-type="WEB" 
        sequence="100000002" />
        <body>
        <info mode="3" 
        value 
        count="40" 
        />
        </body>
        </message>'''

    de_info = '''<?xml version="1.0" encoding="UTF-8" ?>
<message module="CDN" version="3.0">
<header action="REQUEST" 
command="CMS_CONTENT_DELETE" sequence="456870674209705737" component-id="ShangHai-OTT-Root-GCM-01" 
component-type="WEB" /><body><contents><content id="xxxx" cache-id="" delete-disk-file="0" />
</contents></body></message>'''
    
    value = 'value="' + REP + '||' + id + '"'
    newinfo = info.replace('value',value)
    req = urllib2.Request(url,newinfo)
    response = urllib2.urlopen(req)
    message = response.read()
    a = message.find('OK')
    if a != -1:
        start = message.find('content id=')
        end = message.find('" content',start)
        content_id = message[start + 12:end]
        newde_info = de_info.replace('xxxx',content_id)
        delereq = urllib2.Request(url,newde_info)
        deleres = urllib2.urlopen(delereq)
        delemes = deleres.read()
        delstatus = "1" 
    else:
        delstatus = "0"
    return delstatus

url = 'http://x.x.x.x:x'

nowtime = time.strftime('%Y-%m-%d %H:%M')
agotime = ((datetime.datetime.now()-datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M"))
sql = "SELECT T2.PORTAL_URL,T1.CHANNEL_CODE from CMS_CONTENT t2,CMS_CONTENT_DELIVERY_HIS t1 where T2.ID=T1.CONTENT_ID AND \
 T1.COMPLETE_TIME > to_date('" + agotime + "'," + "'yyyy-mm-dd hh24:mi') AND T1.COMPLETE_TIME < to_date('" + nowtime + "'," + " 'yyyy-mm-dd hh24:mi')"

#print sql
#time.sleep(10)
conn = cx_Oracle.connect('xxx/xxx@x.x.x.x:1521/media')
cursor = conn.cursor ()  
cursor.execute (sql)  
rows = cursor.fetchall()
now = time.strftime('%Y-%m-%d')
delivery = 'delivery'+ '-'+ now + '.txt'
pwd = '/opt/script/cncms-delivery/'+ delivery
pwdf = '/opt/script/cncms-delivery/'+ 'fail.txt'
pwdu = '/opt/script/cncms-delivery/'+ 'update.txt'
#print pwdu 
#time.sleep(10)

for i in rows:
    id = i[0]
    channel = i[1]
    if channel == "ysten_delivery":
       b = delete(id,'ysten_REP')
       query = ysten(id)  
      # print query
       print b
    elif channel == "bstvod_delivery":
       b = delete(id,'bstvod')
       query = bst(id)
       #print query
       print b
    elif channel == "miguvod_delivery":
       b = delete(id,'migu_REP')
       query = migu(id)
       #print query
       print b
    elif channel == "cmcc_delivery":
       b = delete(id,'cmcc_REP')
       query = cmcc(id)
       #print query
       print b
    elif channel =="test_delivery":
       b = delete(id,'test_REP')
       query = test(id)
       #print query
       print b
    else:
        continue
    
    req = urllib2.Request(url,query)
    response = urllib2.urlopen(req)
    message = response.read()
    print message
    a = message.find('OK')
    if a == -1:
        fail = open(pwdf,'a+')
        fail.write(id + '\n')
        print i
        fail.close()
    time.sleep(0.5)
  
    if b == "1":
       # 1 is update  0 is delivery
       file = open(pwdu,'a+')
       file.write(id + ' ')
       file.write(channel + '\n')
       file.close()
    else:
       file = open(pwd,'a+')
       file.write(id + ' ')
       file.write(channel + '\n')
       file.close()
       
       
二、lcmid-lookup
       
#!/usr/bin/env python

import os
import sys
import urllib
import urllib2
import time
import re
url = 'http://x.x.x.x:x'
file = open('txt')
line = file.readlines()
file.close()
info_query = '''<?xml version="1.0" encoding="UTF-8"?>
<message module="CDN" version="3.0">
        <header action="REQUEST" command="CONTENT_INFO_QUERY" component-id="cnoss01" component-type="WEB" 
        sequence="100000002" />
        <body>
        <info mode="3" 
        value="yyyy||xxxx" 
        count="40" 
        />
        </body>
        </message>'''
for i in line:
    id = i.split()[0]
    channel = i.split()[1]
    newquery = info_query.replace('xxxx',id)
    
    if channel == "miguvod_delivery":
        newquery1 = newquery.replace('yyyy',"migu_REP")
        #print newquery1
    elif channel == "bstvod_delivery":
        newquery1 = newquery.replace('yyyy',"bstvod")
        #print newquery1
    elif channel == "ysten_delivery":
        newquery1 = newquery.replace('yyyy',"ysten_REP")
        #print newquery1
    elif channel == "cmcc_delivery":
        newquery1 = newquery.replace('yyyy',"cmcc_REP")
        #print newquery1
    else:
        continue
    req = urllib2.Request(url,newquery1)
    response = urllib2.urlopen(req)
    message = response.read()
    #print message
    a = message.find('OK')
    #print a
    if a == -1:
        #start = message.find('content id=')
        #end = message.find('" content',start)
        #id = message[start + 12:end]
        print id
    time.sleep(1)

       
 三、http-check
 
#!/usr/bin/env python

import urllib2
import time

def check(id,channel):
    try:    
        url = "http://x.x.x.x:3301/1111.ts?channel-id=" + channel + "&Contentid=" + id +"&stbId=12345678&owsid=1111"
        print url
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        status = response.getcode()
        print  status 
        if status == 200:
            sucess = open('sucessid','a+')
            print >> sucess,id
            sucess.close()
    except urllib2.HTTPError, e:
        print e.code
        fail = open('failid','a+')
        print >> fail,id
        fail.close()
#check('300188759','cmcc')

file = open('txt','r+')
line = file.readlines()
file.close()
for i in line:
    id = i.split()[0]
    channel = i.split()[1]
    if channel == "ysten_delivery":
        check(id,'ysten')
        time.sleep(1)
    elif channel == "cmcc_delivery":
        check(id,'cmcc')
        time.sleep(1)
    else:
        continue



四、hls-check.sh

#!/bin/bash

while read id channle
do
url="http://x.x.x.x:3302/1.m3u8?channel-id=&owsid=111&stbId=checke&Contentid="
bst="bstvod_delivery"
migu="miguvod_delivery"

check (){
    uri="http://x.x.x.x:3302"
    wget  -T 10 -t 3 "$1"  -O  ./checktest/$2.m3u8
    if [ $? -eq 0 ]
    then
        tsname=`grep "ts" ./checktest/$2.m3u8 |tail -1`
        newuri=`echo $uri"/""$tsname"`
        echo $newuri
        wget "$newuri" -t 2 -T 10  -O  ./checktest/$2.ts
     if [ $? -eq 0 ]
     then
         echo $2 >> ./sucess.txt
     else
         echo $2 >> ./fail.txt
     fi

else
     echo $2 >>fail.txt
fi
}

if [ "$channle" == "$bst" ]
then
    newurl="http://x.x.x.x:3302/1.m3u8?channel-id=bstvod&owsid=111&stbId=checke&Contentid=$id"
    echo $id
    check $newurl $id
    
elif [ "$channle" == "$migu" ]
then 
    newurl="http://x.x.x.x:3302/1.m3u8?channel-id=miguvod&owsid=111&stbId=checke&Contentid=$id"
   echo $id
   check $newurl $id
else
   continue
fi
   
rm -rf ./checktest/*
sleep 1

done < ./txt



