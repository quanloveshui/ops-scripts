from datetime import datetime, timedelta
import os
import commands
import ftplib
from ftplib import FTP

GSLB_LOG = "/usr/local/log/zabbix"
GSLB_ORIGIN_LOG = "/usr/local/log"
#GSLB_ORIGIN_LOG_HTTPS = "/usr/local/log/https"
SPLIT_LOG = "debug."
FTP_SERVER="x.x.x.x"
FTP_USERNAME="xxxxx"
FTP_PASSWORD="xxxxxZ"
FTP_DIR="gslb_x.x.x.x"


class SplitGSLBLog(object):

    def __init__(self):
        split_time = datetime.now() - timedelta(minutes=1)
        self._day_time = ("%d_%02d_%02d") % (split_time.year, split_time.month, split_time.day)
        self._hour_time = ("%02d") % (split_time.hour)
        self._minute_time = ("%02d") % (split_time.minute)
        self._minute_dir = ("%02d") % (split_time.minute - split_time.minute % 5)
        self._do_job()
        
    def _ftp_upload_file(self, log_dir, log_file, dest_file) : #log_dir:/usr/local/log   log_file:debug.202003261000.log dest_file:debug.202003261000.log
        try:
            ftp = FTP()
            ftp.connect(FTP_SERVER)
            ftp.login(FTP_USERNAME, FTP_PASSWORD)
            bufsize = 1024
            fp = open(log_dir+'/'+log_file, 'rb')
            ftp.storbinary('STOR '+ FTP_DIR+'/'+dest_file,fp,bufsize) #上传到ftp的/home/pbsgslblog/ftp/gslb_10.186.59.178目录下面
            fp.close()
            ftp.quit()
        except ftplib.all_errors:
            return 1 
            
        return 0

    def _do_job(self):
        self._get_log_dir()#创建目录/usr/local/log/zabbix/2020_03_26/00/00
        self._split_gslb_origin_log()
        pass

    def _split_gslb_origin_log(self):
        log_list = self._get_log_list(GSLB_ORIGIN_LOG) #log_list: ['debug.202003261000.log','debug.202003261001.log']
        for log in log_list:
            if not log:
                continue
            self._get_real_log_dir(log)
            commands.getoutput('cp '+GSLB_ORIGIN_LOG+'/'+log+' '+self._real_log_dir+'/'+log)
            up_rlt = self._ftp_upload_file(GSLB_ORIGIN_LOG, log, log)
            if up_rlt!=0:
                #cp log when upload failed
                continue
            pass
            commands.getoutput('mv -f '+GSLB_ORIGIN_LOG+'/'+log+' '+self._real_log_dir+'/'+log)
        pass
        #log_list = self._get_log_list(GSLB_ORIGIN_LOG_HTTPS)
        #for log in log_list:
            #if not log:
            #    continue
           # self._get_real_log_dir(log)
            #commands.getoutput('cp '+GSLB_ORIGIN_LOG_HTTPS+'/'+log+' '+self._real_log_dir+'/https'+log)
            #up_rlt = self._ftp_upload_file(GSLB_ORIGIN_LOG_HTTPS, log, 'https'+log)
           # if up_rlt!=0:
                #cp log when upload failed
             #   continue
            #pass
            #commands.getoutput('mv -f '+GSLB_ORIGIN_LOG_HTTPS+'/'+log+' '+self._real_log_dir+'/https'+log)
       # pass
        
    def _get_real_log_dir(self, log_file): #log_file:debug.202003261000.log
        year = log_file[6:10]
        mon  = log_file[10:12]
        day  = log_file[12:14]
        hour = log_file[14:16]
        min  = log_file[16:18]

        self._day_time_r = year+'_'+mon+'_'+day
        self._hour_time_r = hour
        self._minute_time_r = min
        self._minute_dir_r = ("%02d") % (long(self._minute_time_r) - long(self._minute_time_r) % 5)
        self._real_log_dir = GSLB_LOG+'/'+ self._day_time_r+'/'+self._hour_time_r+'/'+self._minute_dir_r  #/usr/local/log/zabbix/2020_03_26/00/00
        
        if not os.path.exists(self._real_log_dir):
            commands.getoutput('mkdir -p '+ self._real_log_dir)
        pass


    def _get_log_dir(self):
        self._gslb_log_dir = GSLB_LOG+'/'+ self._day_time+'/'+self._hour_time+'/'+self._minute_dir
        if not os.path.exists(self._gslb_log_dir):
            commands.getoutput('mkdir -p '+ self._gslb_log_dir)
        pass


    def _get_log_list(self, log_dir):#log_dir:/usr/local/log
        log_list = [] # ['debug.202003261000.log','debug.202003261001.log']
        if os.path.isdir(log_dir):
            for log_name in os.listdir(log_dir):
                if log_name.startswith(SPLIT_LOG):
                    log_list.append(log_name)
        return log_list


if __name__ == '__main__':
    SplitGSLBLog()
