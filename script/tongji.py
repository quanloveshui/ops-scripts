#!/usr/bin/env python
#coding=utf-8


"""统计gslb日志 use:
   tongji.py 2018_11_01/00/00/debug.201811010000.log
   tongji.py 2018_11_01/00/00/debug.201811010000.log 10.200.207.106
   tongji.py 2018_11_01/00/\*/\*  
   tongji.py 2018_11_01/\*/\*/\*
Usage: 
  tongji.py  FILE  [HOST]...
  tongji.py -h | --help
  tongji.py --version
Arguments:
  FILE        log file  
  HOST        host ip  default is all vod cache
Options:
  -h --help
  -v --version
"""



from docopt import docopt
import paramiko
import sys
import os
import re
import socket

reload(sys)
sys.setdefaultencoding('utf8')

 
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
 
 


def cli():
    arguments = docopt(__doc__,version='tongji 1.0')
    #print arguments
    #local_ip = os.popen("ifconfig| grep bond0 -A 1| grep -oP '(?<=inet )[\d\.]+'")
    #p = re.compile(r'(?:(?:[01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){3}(?:[01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])')
    log = arguments["FILE"]
    if len(arguments["HOST"]) != 0:
        hosts = arguments["HOST"]
    else:
        hosts = ["10.200.207.106","10.200.207.107","10.200.207.111"]
    u = "version"
    w = "2wsx@WSX"
    log_dir = '/usr/local/log/zabbix/'
    log = log_dir + log
    for h in hosts:
        #if h != local_ip:
         #   log=re.sub(r'(?:(?:[01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){3}(?:[01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])', h, log)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((h, 22))
        if result == 0:
            p = 22
        else:
            p = 5188
        sock.close()
        obj = SSHParamiko(h, p, u, w)
        cmd_ip = ["less %s| awk -F '|' '{print $16}'|sort|uniq -c|sort -nr|head -5" % (log),"访问IP最多"]
        cmd_contentid = ["less %s |awk -F '|' '{print $19}'  | sort|uniq -c|sort -nr|head -5" % (log),"访问内容最多"]
        cmd_chanelid = ["less %s  |awk -F '|' '{print $17}'|sort|uniq -c|sort -nr|head -5" % (log),"访问牌照方最多"]
        for cmd in [cmd_ip,cmd_contentid,cmd_chanelid]:
            r = obj.run_cmd(cmd[0])
            #print(r[0])
            print("%s  %s 查询结果如下:") % (h,cmd[1])
            print r[1]
    
        
if __name__ == '__main__':
    cli()
