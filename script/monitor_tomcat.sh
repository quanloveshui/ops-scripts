#!/bin/bash
#自动监控tomcat进程，挂了就执行重启操作

#定义环境变量
export JAVA_HOME=/usr/local/jdk-6u45
export JRE_HOME=/usr/local/jdk-6u45/jre
export PATH=/usr/local/jdk-6u45/bin:/usr/lib64/qt-3.3/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/redis/bin/:/root/bin

#check tomcat process
num=`ps -ef | grep tomcat | grep -v 'grep'| wc -l`
#log dir
TomcatMonitorLog=/opt/script/TomcatMonitor.log

Monitor()
{
     if [ "$num" = 0 ]
     then
         echo "[error]进程不存在!tomcat将重启..."
         date
         echo "############stop tomcat###################################"
         killall java   
         sleep 3
         echo "##########start tomcat####################################"
         cd /usr/local/apache-tomcat-6.0.53/bin/ && ./startup.sh
         TomcatID=`ps -ef |grep tomcat |grep -v 'grep'|awk '{print $2}'`
         if [ $TomcatID ];then
             echo "####tomcat start sucess , tomcat进程ID为:$TomcatID####"
         fi
    fi

}

Monitor>>$TomcatMonitorLog
