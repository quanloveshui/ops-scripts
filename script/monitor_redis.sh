#!/bin/bash
#monitor redis process

#定义环境变量
export PATH=/usr/local/jdk-6u45/bin:/usr/lib64/qt-3.3/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/redis/bin/:/root/bin

#redis process
redis_status=`ps -ef | grep redis|grep "redis-server"|grep -v grep|awk '{print $2}'`

#monitor log
RedisMonitorLog=/opt/script/RedishMonitor.log

if [  $redis_status ]
then 
    echo "redis  is work" > /dev/null 2>&1
else
    echo -e "##### redis isn't work, restart now !!! #####">>$RedisMonitorLog
    date >>$RedisMonitorLog
    service redis stop
    service redis start
    redis_id=`ps -ef | grep redis|grep "redis-server"|grep -v grep|awk '{print $2}'`
    if [ $redis_id ];then
             echo "####redis start sucess , redis进程ID为:$redis_id####" >>$RedisMonitorLog
         fi

fi
