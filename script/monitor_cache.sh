#!/bin/sh
#上海移动cache守护script

# Check if the cache pid is exist
uc=$(ps -ef | grep cache | grep -v grep | wc -l)
#echo $uc
if [ "$uc" = 0 ]
then
echo "### cache is core! ###"
date
sh /data/2restart_cache.sh
fi

二、2restart_cache.sh
#!/bin/sh

ps -ef | grep cache
cd /opt/contex/cache/bin/
./owcache.sh stop

sleep 1
ps -ef | grep cache

RTIME=`date +%Y%m%d%H%M%S`
mv /data/syslog/crm /data/syslog/${RTIME}crm
mv /data/syslog/ccm /data/syslog/${RTIME}ccm
mv /data/syslog/userver /data/syslog/${RTIME}userver
mv /opt/contex/cache/bin/log /opt/contex/cache/bin/${RTIME}log
mkdir /data/syslog/userver /data/syslog/crm /data/syslog/ccm /opt/contex/cache/bin/log
chmod 777 /data/syslog/*

cd /opt/contex/cache/bin/
./owcache.sh start

sleep 1
ps -ef | grep cache
