from datetime import datetime, timedelta
import os
import commands
import time
import ftplib
from ftplib import FTP

GSLB_KAFKA_LOG = "/home/kafka"
GSLB_KAFKA_TMP_LOG = "/home/kafka_tmp"
GSLB_ORIGIN_LOG = "/home/pbsgslblog/ftp"
SPLIT_LOG = "debug."
SPLIT_LOG_HTTPS = "httpsdebug."
FTP_SERVER="x.x.x.x"
FTP_USERNAME="xxxx"
FTP_PASSWORD="xxxxxxx"
FLUME_MAJOR=[ 'x.x.x.x','x.x.x.x']


FLUME_MINOR=[ 'x.x.x.x','x.x.x.x' ] 



class SplitGSLBLog(object):

    def __init__(self):
        split_time = datetime.now() - timedelta(minutes=1)
        self._day_time = ("%d_%02d_%02d") % (split_time.year, split_time.month, split_time.day)
        self._hour_time = ("%02d") % (split_time.hour)
        self._minute_time = ("%02d") % (split_time.minute)
        self._minute_dir = ("%02d") % (split_time.minute - split_time.minute % 5)
        self._do_job()
        
    def _ftp_upload_file(self, log_dir, log_file) : #log_dir:gslb_10.186.59.125  log:debug.202003261000.log
        try:
            ftp = FTP()
            ftp.connect(FTP_SERVER)
            ftp.login(FTP_USERNAME, FTP_PASSWORD)
            bufsize = 1024
            #print(GSLB_ORIGIN_LOG+'/'+log_dir+'/'+log_file)
            fp = open(GSLB_ORIGIN_LOG+'/'+log_dir+'/'+log_file, 'rb') #打开local file
            ftp.storbinary('STOR '+ log_dir+'/'+log_file,fp,bufsize) #远程
            fp.close()
            ftp.quit()
        except ftplib.all_errors:
            return 1
            
        return 0

    def _do_job(self):
        #self._get_log_dir()
        
        if os.path.isdir(GSLB_ORIGIN_LOG):
            for log_dir in os.listdir(GSLB_ORIGIN_LOG):
                #print(self._day_time+' '+self._hour_time+':'+self._minute_time+'  scan dir '+GSLB_ORIGIN_LOG+'/'+log_dir)
                is_valid = self._is_valid_dir(FLUME_MAJOR, log_dir) # 判断gslb_10.186.59.125是不是在FLUME_MAJOR里面，如果在继续
                if is_valid==0:
                    continue
                pass
                #print(self._day_time+' '+self._hour_time+':'+self._minute_time+'  scan dir '+GSLB_ORIGIN_LOG+'/'+log_dir)
                if os.path.isdir(GSLB_ORIGIN_LOG+'/'+log_dir): 
                    self._split_gslb_origin_log(log_dir)#log_dir:gslb_10.186.59.125
                pass
            pass
 
        pass

    def _split_gslb_origin_log(self, log_dir):#log_dir:gslb_10.186.59.125
        log_list = self._get_log_list(GSLB_ORIGIN_LOG+'/'+log_dir) #log_list :['debug.202003261000.log','debug.202003261001.log']
        
        filecnt=0
       
        for log in log_list:
            if not log:
                continue
            filecnt=filecnt+1
            if filecnt>5 :
                time.sleep(0.1)
            pass
            if filecnt>30 :
                print('more than 30 file in '+log_dir+'/'+log);
                break
            pass
            up_rlt = self._ftp_upload_file(log_dir, log)#log_dir:gslb_10.186.59.125  log:debug.202003261000.log
            if up_rlt!=0:
                #not mv log when upload failed
                print('fail to upload '+log_dir+'/'+log)
                continue
            pass
            print('upload file '+log_dir+'/'+log)
            self._get_real_log_dir(GSLB_ORIGIN_LOG+'/'+log_dir, log)
            #commands.getoutput('cp '+GSLB_ORIGIN_LOG+'/'+log_dir+'/'+log+' '+GSLB_KAFKA_LOG+'/'+log_dir+'/'+log)
            #print('cp '+GSLB_ORIGIN_LOG+'/'+log_dir+'/'+log+' '+GSLB_KAFKA_LOG+'/'+log_dir+'/'+log)
            commands.getoutput('cp '+GSLB_ORIGIN_LOG+'/'+log_dir+'/'+log+' '+self._real_log_dir+'/'+log)
            print('cp '+GSLB_ORIGIN_LOG+'/'+log_dir+'/'+log+' '+self._real_log_dir+'/'+log)
            commands.getoutput('mv '+GSLB_ORIGIN_LOG+'/'+log_dir+'/'+log+' '+GSLB_KAFKA_TMP_LOG+'/'+log_dir+'/'+log)
            print('mv '+GSLB_ORIGIN_LOG+'/'+log_dir+'/'+log+' '+GSLB_KAFKA_TMP_LOG+'/'+log_dir+'/'+log)
            commands.getoutput('mv '+GSLB_KAFKA_TMP_LOG+'/'+log_dir+'/'+log+' '+GSLB_KAFKA_LOG+'/'+log_dir+'/'+log)
            print('mv '+GSLB_KAFKA_TMP_LOG+'/'+log_dir+'/'+log+' '+GSLB_KAFKA_LOG+'/'+log_dir+'/'+log)
        pass
        
    def _get_real_log_dir(self, log_dir, log_file):#log_dir:gslb_10.186.59.125  log:debug.202003261000.log
        idx = 0
        if log_file.startswith(SPLIT_LOG_HTTPS):
            idx = 5

        year = log_file[idx+6:idx+10]
        mon  = log_file[idx+10:idx+12]
        day  = log_file[idx+12:idx+14]
        hour = log_file[idx+14:idx+16]
        min  = log_file[idx+16:idx+18]

        self._day_time_r = year+'_'+mon+'_'+day
        self._hour_time_r = hour
        self._minute_time_r = min
        self._minute_dir_r = ("%02d") % (long(self._minute_time_r) - long(self._minute_time_r) % 5)
        self._real_log_dir = log_dir+'/'+ self._day_time_r+'/'+self._hour_time_r+'/'+self._minute_dir_r
        
        if not os.path.exists(self._real_log_dir):
            commands.getoutput('mkdir -p '+ self._real_log_dir)
        pass

    def _get_log_list(self, log_dir): #log_dir:/home/pbsgslblog/ftp/gslb_10.186.59.125
        log_list = []# ['debug.202003261000.log','debug.202003261001.log']
        if os.path.isdir(log_dir):
            for log_name in os.listdir(log_dir):
                if log_name.startswith(SPLIT_LOG) or log_name.startswith(SPLIT_LOG_HTTPS):
                    log_list.append(log_name)
        return log_list

    def _is_valid_dir(self, dir_list, log_dir):
        for log_item in dir_list:
            if log_dir==log_item :
                return 1
            pass
        pass
        
        return 0


if __name__ == '__main__':
    SplitGSLBLog()
