#!/usr/bin/env python
#coding=utf-8

import paramiko
import sys
import time,datetime
import os
import socket
import re

#定义检查性能指标的类
class SSHParamiko(object):

    err = "argument passwd or rsafile can not be None"

    def __init__(self, host, port, user, passwd=None, rsafile=None):
        self.h = host
        self.p = port
        self.u = user
        self.w = passwd
        self.rsa = rsafile

    def _connect(self):
        if self.w:
            return self.pwd_connect()
        elif self.rsa:
            return self.rsa_connect()
        else:
            raise ConnectionError(self.err)

    def _transfer(self):
        if self.w:
            return self.pwd_transfer()
        elif self.rsa:
            return self.rsa_transfer()
        else:
            raise ConnectionError(self.err)


    def pwd_connect(self):
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(self.h, self.p, self.u, self.w)
        return conn



    def run_cmd(self, cmd):
        conn = self._connect()
        stdin, stdout, stderr = conn.exec_command(cmd)
        code = stdout.channel.recv_exit_status()
        stdout, stderr = stdout.read(), stderr.read()
        conn.close()
        if not stderr:
            return code, stdout.decode()
        else:
            return code, stderr.decode()

    #检查磁盘使用率
    def check_disk(self):
        l = [] #存放使用率超过80%的磁盘
        l_all = []#存放所有的磁盘使用情况
        conn = self._connect()
        cpu_cmd = "df -hP | grep -v 文件系统 | grep -v Filesystem |grep -v docker| awk '{print $5,$6}'"
        stdin, stdout, stderr = conn.exec_command(cpu_cmd)
        stdout, stderr = stdout.read(), stderr.read()
        conn.close()
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
        conn = self._connect()
        cpu = "vmstat 1 3|sed  '1d'|sed  '1d'|awk '{print $15}'"
        stdin, stdout, stderr = conn.exec_command(cpu)
        cpu = stdout.readlines()
        cpu_idle = int((int(cpu[0]) + int(cpu[1]) + int(cpu[2])) / 3)
        cpu_use = 100-cpu_idle
        return cpu_use



    #检查内存和swap使用率
    def check_mem(self):
        conn = self._connect()
        mem_cmd = "cat /proc/meminfo"
        stdin, stdout, stderr = conn.exec_command(mem_cmd)
        mem = stdout.read().decode('utf-8')
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
    def check_process(self,host):
        lvs = ['10.200.207.109','10.200.207.110']
        conn = self._connect()
        if host in lvs:
            cmd_process = 'ps -ef | grep keepalived| grep -v grep | wc -l'
        else:
            cmd_process = 'ps -ef | grep java| grep -v grep | wc -l'
        stdin, stdout, stderr = conn.exec_command(cmd_process)
        status = stdout.read()
        status = str(status.strip())
        return status

    #检查ping网关是否通 0 代表通
    def check_gateway(self):
        conn = self._connect()
        cmd_gate = "/usr/sbin/route -n | grep UG | awk '{print $2}'"
        stdin, stdout, stderr = conn.exec_command(cmd_gate)
        gateway = stdout.read()
        stdin, stdout, stderr = conn.exec_command("/usr/bin/ping -c 1 -w 1 %s| grep transmitted|awk '{print $6}'" % gateway.strip())
        status = stdout.read()
        status = status.split('%')[0]
        return status
   
    
    #检查安全日志
    def check_log(self):
        conn = self._connect()
        cmd_log = 'tail -1000 /var/log/messages |grep -i -e warning  -e panic -e fail |grep -v -e "crossed links" -e "user_cmd"|egrep -v ".sh|successful|received invalid message|Raw_Read_Error_Rate|Recovered Error"'
        stdin, stdout, stderr = conn.exec_command(cmd_log)
        log = stdout.read()
        log = log.strip()
        return log
        
        

if __name__ == '__main__':
    h = ["192.168.0.1","192.168.0.2"]
    p = 22
    u = "xxxx"
    w = "xxxx"
    result = [] 
    sucess = []
    waring = []
    dirs = '/home/xunjian/'
    if os.path.exists(dirs):
        pass
    else:
        os.makedirs(dirs)

    

    for i in h:
        tmp = {}
        obj = SSHParamiko(i, p, u, w)
        res_disk = obj.check_disk()
        res_cpu = obj.check_cpu()
        res_mem = obj.check_mem()
        res_pro = obj.check_process(i)
        res_gateway = obj.check_gateway()
        res_log = obj.check_log()

        if len(res_disk[0]) > 0:
            tmp = {i:{'disk':res_disk[0]}}
        if res_cpu >= 80:
           if tmp.has_key(i):
               tmp[i]['cpu'] = res_cpu
           else:
               tmp = {i:{'cpu':res_cpu}}
        if res_mem[0] >= 80:
            if tmp.has_key(i):
                tmp[i]['Mem'] = res_mem[0]
            else:
                tmp = {i:{'Mem':res_mem[0]}}
        if res_mem[1] >= 80:
            if tmp.has_key(i):
                tmp[i]['Swap'] = res_mem[1]
            else:
                tmp = {i:{'Swap':res_mem[1]}}
        if res_pro == '0':
            if tmp.has_key(i):
                tmp[i]['process'] = 'java or keepalived process does not exist'
            else:
                tmp = {i:{'process':'java or keepalived process does not exist'}}
        if res_gateway != '0':
            if tmp.has_key(i):
                tmp[i]['ping'] = 'Ping the gateway is not available'
            else:
                tmp = {i:{'ping':'Ping the gateway is not available'}}
        if res_log != '':
           if tmp.has_key(i):
               tmp[i]['log'] = res_log
           else:
               tmp = {i:{'log':res_log}}
        if tmp:
            waring.append(tmp) #异常信息存入列表 {'10.200.207.106':{'Mem':90}}
        if len(res_disk[0]) == 0 and res_cpu < 80 and res_mem[0] < 80 and res_mem[1] < 80 and res_pro != '0' and res_gateway == '0' and res_log == '':
            sucess.append(i) #无任何告警信息的主机ip存入列表
        #主机所有巡检信息存入列表
        result.append({i:{'disk':res_disk[1],'cpu':res_cpu,'Mem':res_mem[0],'Swap':res_mem[1],'process':res_pro,'ping':res_gateway,'log':res_log}})
         

    filename = dirs + datetime.datetime.now().strftime('%Y%m%d') + '.txt'
    f = open(filename,'w+')            
    #print(sucess)
    #print(waring)
    f.write('{0:*^80}'.format('本次巡检结果如下')+'\r\n')
    f.write('本次巡检时间:{}'.format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M'))+'\r\n')
    f.write('本次巡检服务器共{}台'.format(len(h)) +'\r\n')
    f.write('本次巡检无告警共{}台'.format(len(sucess)) +'\r\n')
    f.write('本次巡检有告警共{}台'.format(len(waring)) +'\r\n')
    #写入巡检有告警的信息
    if len(waring) == 0:
        f.write('本次巡检完成，所有服务器均正常，请放心'+'\r\n')
    else:
        f.write('{0:*^80}'.format('本次巡检告警信息如下')+'\r\n')
        for i in waring:
            host = i.keys()
            v = i.values()
            print('主机%s的告警信息如下:' % host[0])
            f.write('主机%s的告警信息如下:' % host[0] +'\r\n')
            for k1,v1 in v[0].items():
                if k1 == 'disk':
                    print('{:>8}磁盘目前使用率为{},已经超过80%,请检查确认'.format('',v1))
                    f.write('{:>8}磁盘目前使用率为{},已经超过80%,请检查确认'.format('',v1)+'\r\n')
                if k1 == 'cpu':
                    print('{:>8}CPU目前使用率为{}%,已经超过80%,请检查确认'.format('',v1))
                    f.write('{:>8}CPU目前使用率为{}%,已经超过80%,请检查确认'.format('',v1)+'\r\n')
                if k1 == 'Mem':
                    print('{:>8}Mem目前使用率为{}%,已经超过80%,请检查确认'.format('',v1))
                    f.write('{:>8}Mem目前使用率为{}%,已经超过80%,请检查确认'.format('',v1)+'\r\n')
                if k1 == 'Swap':
                    print('{:>8}Swap目前使用率为{}%,已经超过80%,请检查确认'.format('',v1)) 
                    f.write('{:>8}Swap目前使用率为{}%,已经超过80%,请检查确认'.format('',v1)+'\r\n')
                if k1 == 'process':
                   print('{:>8}java or keepalived 进程不存在,请检查确认'.format(''))
                   f.write('{:>8}java or keepalived 进程不存在,请检查确认'.format('')+'\r\n')
                if k1 == 'ping':
                   print('{:>8}ping 网关不通,请检查确认'.format(''))
                   f.write('{:>8}ping 网关不通,请检查确认'.format('')+'\r\n')
                if k1 == 'log':
                   f.write('{:>8}系统报错日志:{},请检查确认'.format('',v1)+'\r\n')

    #写入所有巡检结果
    f.write('{0:*^80}'.format('所有主机完整巡检结果如下')+'\r\n')
    for i in result:
        host = i.keys()
        v = i.values()
        f.write('主机%s的完整巡检结果如下:' % host[0] +'\r\n')
        for k1,v1 in v[0].items():
            if k1 == 'disk':
                f.write('{:>8}磁盘目前使用率为:'.format('')+'\r\n')
                for j in v1:
                    f.write('{:>8}{}'.format('',j)+'\r\n')
            if k1 == 'cpu':
                f.write('{:>8}CPU目前使用率为:{}%'.format('',v1)+'\r\n')
            if k1 == 'Mem':
                f.write('{:>8}Mem目前使用率为:{}%'.format('',v1)+'\r\n')
            if k1 == 'Swap':
                f.write('{:>8}Swap目前使用率为:{}%'.format('',v1)+'\r\n')
            if k1 == 'process':
                f.write('{:>8}java or keepalived 进程状态为:{}  (0 代表进程状态异常)'.format('',v1)+'\r\n')
            if k1 == 'log':
                f.write('{:>8}系统报错日志:{}   (没有内容代表没报错信息)'.format('',v1)+'\r\n')
            if k1 == 'ping':
                f.write('{:>8}ping 网关结果:{}  (0 代表到网关通)'.format('',v1)+'\r\n')
    f.close()
    print("本次巡检已经完成,巡检信息已经写入{}文件中,请查看".format(filename))
