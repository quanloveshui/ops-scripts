#!/usr/bin/env python
#coding=utf-8

import commands
import sys
import time,datetime
import os
import socket
import re
import socket
import json

#定义检查性能指标的类
class LSDN_CHECK(object):
    def run_cmd(self, cmd):
        status,res_type=commands.getstatusoutput(cmd)
        return status,res_type

    #检查磁盘使用率
    def check_disk(self):
        l = [] #存放使用率超过80%的磁盘
        l_all = []#存放所有的磁盘使用情况
        disk_cmd = "df -hP | grep -v 文件系统 | grep -v Filesystem |grep -v docker| awk '{print $5,$6}'"
        code,stdout = self.run_cmd(disk_cmd)
        result = stdout.decode()
        result = result.split('\n')
        for i in result:
            if i:
                i = i.encode('utf-8')
                l_all.append(i)
                use,disk = tuple(i.split())
                use = use.split('%')[0]
                if int(use) > 80: #输出使用率超过80%
                    l.append(i)
            else:
                continue
        return l,l_all

    #检查CPU使用率
    def check_cpu(self):
        cpu_cmd = "vmstat 1 3|sed  '1d'|sed  '1d'|awk '{print $15}'"
        code,stdout = self.run_cmd(cpu_cmd)
        cpu = stdout.split('\n')
        cpu_idle = int((int(cpu[0]) + int(cpu[1]) + int(cpu[2])) / 3)
        cpu_use = 100-cpu_idle
        return cpu_use



    #检查内存和swap使用率
    def check_mem(self):
        mem_cmd = "cat /proc/meminfo"
        code,stdout = self.run_cmd(mem_cmd)
        mem = stdout.decode('utf-8')
        aa = re.sub(r' kB','',mem)
        bb = re.sub(r' +','',aa)
        cc = re.sub(r'\n',':',bb)
        dd = cc.split(":")
        meminfo_dic = {}
        while len(dd)>1:
            meminfo_dic[dd[0]]=dd[1]
            del dd[0:2]
        mem_total = round(int(meminfo_dic.get('MemTotal')) / 1024)
        mem_total_free = round(int(meminfo_dic.get('MemFree')) / 1024) + round(int(meminfo_dic.get('Buffers')) / 1024) + round(int(meminfo_dic.get('Cached')) / 1024)
        swap_total = round(int(meminfo_dic.get('SwapTotal')) / 1024)
        swap_free = round(int(meminfo_dic.get('SwapFree')) / 1024)

        mem_usage = round(((mem_total - mem_total_free) / mem_total) * 100, 2)
        try:
            swap_usage = round(((swap_total - swap_free) / swap_total) * 100, 2)
        except:
            swap_usage = 0
        return mem_usage,swap_usage

    #检查进程是否存在,0代表不存在
    def check_process(self):
        cmd_process = 'sudo docker ps|wc -l'
        code,stdout = self.run_cmd(cmd_process)
        status = stdout
        status = str(status.strip())
        return status

    #检查ping网关是否通 0 代表通
    def check_gateway(self):
        cmd_gate = "/usr/sbin/route -n | grep UG | awk '{print $2}'"
        code,stdout = self.run_cmd(cmd_gate)
        gateway = stdout
        code, stdout= self.run_cmd("/usr/bin/ping -c 1 -w 1 %s| grep transmitted|awk '{print $6}'" % gateway.strip())
        status = stdout
        status = status.split('%')[0]
        return status


    #检查安全日志
    def check_log(self):
        cmd_log = 'tail -1000 /var/log/messages |grep -i -e warning  -e panic -e fail |grep -v -e "crossed links" -e "user_cmd"|egrep -v ".sh|successful|received invalid message|Raw_Read_Error_Rate|Recovered Error"'
        code,stdout=self.run_cmd(cmd_log)
        log = stdout
        log = log.strip()
        return log

    def write_file(self,dir,content):
        with open(dir,'w+') as f:
            json.dump(content,f)
    def write_cron(self):
        cmd="sudo crontab -l| grep '/home/migu/day-xunjian.py'|wc -l"
        status,res_type=commands.getstatusoutput(cmd)
        #print(type(res_type))
        if res_type=='0':
            cmd1='sudo crontab -l > /tmp/crontab.tmp'
            cmd2='sudo sh -c  \"echo \'0 10 * * *  python /home/migu/day-xunjian.py\'>> /tmp/crontab.tmp\"'
            cmd3='sudo crontab /tmp/crontab.tmp'
            commands.getoutput(cmd1)
            commands.getoutput(cmd2)
            commands.getoutput(cmd3)

if __name__ == '__main__':
    result = []
    sucess = []
    waring = []
    dirs = '/home/migu/xunjian/'
    hostname=socket.gethostname()
    #filename = '%s%s/%s%s' % (dirs,hostname, datetime.datetime.now().strftime('%Y%m%d'), '.txt')
    filename = '%s%s%s' % (dirs,hostname, '.txt')
    #print(filename)
    if os.path.exists(dirs):
        pass
    else:
        os.makedirs(dirs)



    tmp = {}
    obj = LSDN_CHECK()
    res_disk = obj.check_disk()
    res_cpu = obj.check_cpu()
    res_mem = obj.check_mem()
    res_pro = obj.check_process()
    res_gateway = obj.check_gateway()
    res_log = obj.check_log()
    if len(res_disk[0]) > 0:
        tmp = {hostname:{'disk':res_disk[0]}}
    if res_cpu >= 80:
        if tmp.has_key(hostname):
            tmp[hostname]['cpu'] = res_cpu
        else:
            tmp = {hostname:{'cpu':res_cpu}}
    if res_mem[0] >= 80:
        if tmp.has_key(hostname):
            tmp[hostname]['Mem'] = res_mem[0]
        else:
            tmp = {hostname:{'Mem':res_mem[0]}}
    if res_mem[1] >= 80:
        if tmp.has_key(hostname):
            tmp[hostname]['Swap'] = res_mem[1]
        else:
            tmp = {hostname:{'Swap':res_mem[1]}}
    if res_pro == '0':
        if tmp.has_key(hostname):
            tmp[hostname]['process'] = 'livecdn process does not exist'
        else:
            tmp = {hostname:{'process':'livecdn process does not exist'}}
    if res_gateway != '0':
        if tmp.has_key(hostname):
            tmp[hostname]['ping'] = 'Ping the gateway is not available'
        else:
            tmp = {hostname:{'ping':'Ping the gateway is not available'}}
    if res_log != '':
        if tmp.has_key(hostname):
            tmp[hostname]['log'] = res_log
        else:
            tmp = {hostname:{'log':res_log}}
    if tmp:
        waring.append(tmp) #异常信息存入列表 {'10.200.207.106':{'Mem':90}}
    if len(res_disk[0]) == 0 and res_cpu < 80 and res_mem[0] < 80 and res_mem[1] < 80 and res_pro != '0' and res_gateway == '0' and res_log == '':
        sucess.append(hostname) #无任何告警信息的主机ip存入列表
        #主机所有巡检信息存入列表
    result.append({hostname:{'disk':res_disk[1],'cpu':res_cpu,'Mem':res_mem[0],'Swap':res_mem[1],'process':res_pro,'ping':res_gateway,'log':res_log}})

    res_info=[result,waring,sucess]

    obj.write_file(filename,res_info)
    #rsync_cmd='rsync_cmd='rsync -vzrtopg --delete --progress %s root@192.168.1.1::logs/livecdn/check/%s --password-file=/migu/migu_conf/migu_common/rsync/client.pass  --port=1873 >/dev/null 2>&1' % (filename,hostname)'
    rsync_cmd='rsync -vzrtopg --delete --progress %s root@192.168.1.1::logs/lsdn/check/%s --password-file=/etc/zabbix/xunjian/rsyncd.pass  --port=9000 >/dev/null 2>&1' % (filename,hostname)
    code,stdout=commands.getstatusoutput(rsync_cmd)
    #obj.write_cron()
    #f=open(filename,'r+')
    #a=json.load(f)
    #print(a[0])
