一、
#!/bin/bash
#create by titan 20140518 for log upload

filename=*$(date -d "last-hour" +%Y%m%d_%H)*.log
folderdate=$(date -d "last-hour" +%Y%m%d)
echo $filename


#FTP_SERVER="x.x.x.x"
FTP_SERVER="x.x.x.x"
FTP_PORT="21"
FTP_USER="xxxx"
FTP_PASSWD="xxxx"
R_DIR=cache/$folderdate
L_DIR="/data/log/crm"
L_DIR_m="/data/log/crm_service_monitor"
#APP_LOG_DIR="/tmp"

echo $R_DIR
FTP_UPLOAD() {
  ftp -v -n $FTP_SERVER << FU
  user $FTP_USER $FTP_PASSWD
  binary
  hash
  cd $1
  lcd $2
  prompt
  mput $3
  bye
FU
}

#########################################
FTP_UPLOAD $R_DIR $L_DIR $filename;
sleep 10
FTP_UPLOAD $R_DIR $L_DIR_m $filename;




二、
#!/bin/bash
#create by yqh 20170308 for log upload

filename=*$(date -d "last-hour" +%Y%m%d_%H)*.log
folderdate=$(date -d "last-hour" +%Y%m%d)
echo $filename

ip="127.0.0.1"
R_DIR="/data/provincelog/ReportFTPRoot/gsd/$folderdate/"
L_DIR="/data/log/gsd/"
L_DIR_m="/data/log/gsd_route_monitor/"
L_file=$L_DIR$filename
L_m_file=$L_DIR_m$filename
 
#echo $ip":"$R_DIR

scp -r $L_file  $ip":"$R_DIR
scp -r $L_m_file  $ip":"$R_DIR 
