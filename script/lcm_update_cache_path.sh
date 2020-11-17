
#上海移动lcm实时更新缓存路径
一、
#!/bin/bash

dir="/data/logs/cncms/"
path="/opt/script/lcm-path-update/cncms-delivery/"
nowtime=`date +%Y-%m-%d`
log=$dir"catalina."$nowtime".out"
logid=$path"update-"$nowtime".txt"
#echo $log

#touch $logid
tailf $log | grep  --line-buffered  'header action="REQUEST" command="CMS_CONTENT_DELIVERY"'  -A  11| grep 'content id' | awk -F  '"'   '{print $2}'  >> $logid


二、
#!/usr/bin/env python
import os
import time
import datetime
import urllib
import urllib2
import time
import logging  
import logging.handlers


nowtime = time.strftime('%Y-%m-%d')
logfile = '/opt/script/lcm-path-update/cncms-delivery/'+ 'update' + '-' + nowtime + '.txt'
logsfile = '/opt/script/lcm-path-update/logs/'+ 'log' + '-' + nowtime + '.txt'
LOG_FILE = logsfile
handler = logging.handlers.RotatingFileHandler(LOG_FILE,maxBytes = 10240*10240,backupCount = 5)
fmt = '%(asctime)s %(filename)s %(levelname)s %(name)s %(message)s' 
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler) 
logger.setLevel(logging.DEBUG)

def query(id):
    url = 'http://172.17.91.73:7305'
    info = '''<?xml version="1.0" encoding="UTF-8"?>
<message module="CDN" version="3.0">
<header action="REQUEST" command="CONTENT_INFO_QUERY" component-id="cnoss01" component-type="WEB" sequence="100000001"/>
  <body>
    <info   mode="2" 
    value="yyyy" 
    count="40" />
    </body>
</message>'''
    new_info = info.replace('yyyy',id)
    logger.debug(new_info)
    req = urllib2.Request(url,new_info)
    res = urllib2.urlopen(req)
    mes = res.read()
    logger.debug(mes)
    a = mes.find('OK')
    if a != -1:
        start = mes.find('content-repository-id="')
        end = mes.find('_REP',start)
        channel = mes[start+23:end]
        start1 = mes.find('access-mark="')
        end1 = mes.find('" type',start1)
        access = mes[start1+13:end1]
        logger.info("the content channel-id is: " + channel )
        logger.info("the content access-mark is: " + access )
        status = "1"
    else:
        status = "0"
    return status
    

def dele(id):
    url = 'http://172.17.91.73:7305'
    de_info = '''<?xml version="1.0" encoding="UTF-8" ?>
<message module="CDN" version="3.0">
<header action="REQUEST" 
command="CMS_CONTENT_DELETE" sequence="456870674209705737" component-id="ShangHai-OTT-Root-GCM-01" 
component-type="WEB" /><body><contents><content id="xxxx" cache-id="" delete-disk-file="0" />
</contents></body></message>'''
    newde_info = de_info.replace('xxxx',id)
    logger.debug(newde_info)
    delereq = urllib2.Request(url,newde_info)
    deleres = urllib2.urlopen(delereq)
    delemes = deleres.read()
    logger.debug(delemes)
    
with  open(logfile) as file:
    file.seek(0,2)
    while 1:
        where = file.tell()
        #print where
        line = file.readline()
        if not line:
            time.sleep(1)
            file.seek(where)
        else:
            b = query(line.strip())
            if b == "1":
                logger.info("the content_id path need update: "+ line)
                logger.info("begain update lcm path,the content_id is: " + line)
                dele(line.strip())
            else:
                 logger.info("the content_id path need not update:"+ line)
                 dele(line.strip())


三、
#!/bin/bash

ps -ef | grep lcm-path-update.py| grep -v grep | awk '{print $2}' | xargs kill -9
sleep 0.5
ps -ef | grep update-id.sh| grep -v grep | awk '{print $2}' | xargs kill -9
echo "ready chongqi"
sleep 1
nohup  /opt/script/lcm-path-update/update-id.sh &
sleep 2
nohup  /opt/script/lcm-path-update/lcm-path-update.py &
