#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
import os
import commands
import socket

NGINX_LOG = "/var/log/nginx"
LIVE_LOG = "/var/cdnlogs/src/nginx_logs"


class SplitNginxLog(object):

    def __init__(self):
        split_time = datetime.now() - timedelta(minutes=1)
        self._day_time = ("%d_%02d_%02d") % (split_time.year, split_time.month, split_time.day)
        self._hour_time = ("%02d") % (split_time.hour)
        self._minute_time = ("%02d") % (split_time.minute)
        self._minute_dir = ("%02d") % (split_time.minute - split_time.minute % 5)
        self._do_job()

    def _do_job(self):
        self._get_access_dir()
        #self._split_nginx_log()
        self._split_live_log()
        pass

    def _split_live_log(self):
        live_pid = self._get_live_nginx_pid()
        if live_pid <= 0:
            return False
        log_list = self._get_log_list(LIVE_LOG)
        for log in log_list:
            if not log:
                continue
            nginx_access_name = self._get_access_name(log,True)
            commands.getoutput('mv '+LIVE_LOG+'/'+log+' '+self._nginx_access_dir+'/'+nginx_access_name)
        commands.getoutput('/bin/kill -USR1 '+str(live_pid))
       

    def _split_nginx_log(self):
        log_list = self._get_log_list(NGINX_LOG)
        for log in log_list:
            if not log:
                continue
            nginx_access_name = self._get_access_name(log)
            commands.getoutput('mv '+NGINX_LOG+'/'+log+' '+self._nginx_access_dir+'/'+nginx_access_name)
        commands.getoutput('/bin/kill -USR1 $(cat '+NGINX_PID+')')
        pass

    def _get_access_dir(self):
        self._nginx_access_dir = NGINX_LOG+'/'+ self._day_time+'/'+self._hour_time+'/'+self._minute_dir
        if not os.path.exists(self._day_time):
            commands.getoutput('mkdir -p '+ self._nginx_access_dir)
        pass

    def _get_access_name(self, log_name, is_live=False):
        new_log_name = log_name.replace('access.log', '')
        nginx_access_name = ('live_' if is_live else 'vod_') + new_log_name+socket.gethostname() + '_' + \
                            self._day_time + '_' + self._hour_time + '_' + self._minute_time + '.log'
        print(log_name+'----->'+nginx_access_name)
        return nginx_access_name
        pass

    def _get_log_list(self, log_dir):
        log_list = []
        if os.path.isdir(log_dir):
            for log_name in os.listdir(log_dir):
                if LIVE_LOG == log_dir and log_name == "access.log":
                    continue
                if log_name in ["common_access.log","full_access.log","rtmp_access.log"]:
                    log_list.append(log_name)
        print(log_list)
        return log_list

    def _get_live_nginx_pid(self):
        message = commands.getoutput('ps -ef | grep "nginx: master process ./nginx" | grep -v grep | awk \'{print $2}\'').split('\n')
        if not message:
            return 0
        return message[0]


if __name__ == '__main__':
    SplitNginxLog()
