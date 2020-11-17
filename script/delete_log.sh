一、
#!/bin/bash
cd /opt/bstlive
cat luzhi.txt |while read line
do
#echo $line
cd /opt/bstlive/$line/record
#pwd
>record.log
done


二、
#!/bin/bash
L_DIR="/data/syslog/userver"
rm -f $L_DIR/UServerHawk_APP_INFO.log-*
find /data/log/crm/ -mtime +14 -name "*.log" -exec rm -rf {} \;

三、
#!/bin/bash
TIME=`date -d "1 day ago" +"%Y%m%d"`
cd /data/syslog/userver
rm -f UServerHawk_APP_INFO.log-*
>UServerHawk_APP_INFO.log
#find /data/log/crm/  -name "*$TIME*.log"
find /data/log/crm/  -name "*$TIME*.log" -exec rm -rf {} \;
