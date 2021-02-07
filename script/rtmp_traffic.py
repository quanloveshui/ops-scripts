#!/usr/bin/env python
#分析日志，数据存入influxdb数据库


from __future__ import division  # py2
import commands
import time, os
from datetime import datetime, timedelta

log_path = '/var/log/nginx/'


class Get_rtmp_traffic:
    def __init__(self):
        split_time = datetime.now() - timedelta(minutes=6)
        self._day_time = ("%d_%02d_%02d") % (split_time.year, split_time.month, split_time.day)
        self._hour_time = ("%02d") % (split_time.hour)
        self._minute_time = ("%02d") % (split_time.minute)
        self._minute_dir = ("%02d") % (split_time.minute - split_time.minute % 5)
        self.do_job()

    def do_job(self):
        self.send_info()

    def send_info(self):
        rtmp_path = '%s%s/%s/%s/' % (log_path, self._day_time, self._hour_time, self._minute_dir)
        print(rtmp_path)

        log_list = self.get_log_list(rtmp_path)
        # print(log_list)

        for log in log_list:
            if not log:
                continue
            host, times = self.deal_log_name(log)
            timeStamp = self.deal_time(times)
            timeStamp = timeStamp * 1000000000
            # print(timeStamp)
            traffic_push, traffic_play = self.deal_rtmp_log(rtmp_path + log)
            #print(times)
            # print(traffic_push)
            # print(traffic_play)
            for k, v in traffic_push.items():
                # v=round(v*8/60,3)
                # v=v*8
                cmd = "curl -i  -XPOST 'http://192.168.1.1:8086/write?db=xxx' -u xxx:xxx --data-binary 'lsdn,host=%s,domain=%s push=%s %s'" % (host, k, v, timeStamp)
                status, res = commands.getstatusoutput(cmd)
            for k, v in traffic_play.items():
                cmd = "curl -i  -XPOST 'http://192.168.1.1:8086/write?db=xxx' -u xxx:xxx --data-binary 'lsdn,host=%s,domain=%s play=%s %s'" % (host, k, v, timeStamp)
                status, res = commands.getstatusoutput(cmd)
                # print(res)

    def deal_rtmp_log(self, log):
        traffic_push = {}
        traffic_play = {}
        f = open(log, 'r+')
        lines = f.readlines()
        f.close()
        for line in lines:
            line = line.split('|')
            if line[1] == 'PUBLISH':
                push = line[4].strip()
                push = int(push)
                push = push * 8
                # play=line[5].strip()
                #domain = line[8].strip(':1935')
                if '1935' in line[8]:
                    domain = line[8].strip(':1935')
                else:
                    domain = line[8].strip()
                if domain in traffic_push:
                    traffic_push[domain] += push
                else:
                    traffic_push[domain] = push
            if line[1] == 'PLAY':
                play = line[6].strip()
                play = int(play)
                play = round(play * 8 / 60, 3)
                #domain = line[8].strip(':1935')
                if '1935' in line[8]:
                    domain = line[8].strip(':1935')
                else:
                    domain = line[8].strip()
                if domain in traffic_play:
                    traffic_play[domain] += play
                else:
                    traffic_play[domain] = play

        return traffic_push, traffic_play

    def deal_time(self, times):
        timeArray = time.strptime(times, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        # print(timeArray)
        return timeStamp

    def deal_log_name(self, log_name):
        infos = log_name.split('_')
        host = infos[2:6]
        times = infos[6:]
        host = '_'.join(host)
        times = '%s-%s-%s %s:%s:00' % (times[0], times[1], times[2], times[3], times[4].strip('.log'))
        # print(host,times)
        return host, times

    def get_log_list(self, log_dir):
        log_list = []
        if os.path.isdir(log_dir):
            for log_name in os.listdir(log_dir):
                if log_name.startswith("live_rtmp"):
                    log_list.append(log_name)
        return log_list


if __name__ == '__main__':
    Get_rtmp_traffic()
