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
import requests
import json

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
 
 
#查询IP地理信息
def IpCheck(IP):
    proxies = {
              "http": "x.x.x.x:3128",
    }
    url = "http://www.ip138.com/ips138.asp?ip=%s&action=2"  % str(IP)
    response = requests.get(url, proxies = proxies)
    response.encoding = 'gbk'
    res = response.text
    regex = re.compile('<ul class="ul1"><li>(.*?)</li><li>(.*?)</li><li>(.*?)</li></ul>')
    data = regex.findall(res)[0]
    data = data[0].decode('utf-8').encode('utf-8')
    data = data.split('本站数据：')[1]
    result = '%s  %s' % (IP,data) 
    return result

#获取IP,查询IP信息并格式化输出
def Read_file(txt):
    l_ip = []
    l_num = []
    with open(txt,'r+') as f:
        for i in f.readlines():
            num = i.strip().split()[0]
            ip = i.strip().split()[1]
            res = IpCheck(ip)
            l_ip.append(res)
            l_num.append(num)
            
    ip_info = """
    %s   %s
    %s   %s
    %s   %s
    %s   %s
    %s   %s
              """  %  (l_num[0],l_ip[0],l_num[1],l_ip[1],l_num[2],l_ip[2],l_num[3],l_ip[3],l_num[4],l_ip[4])
    return ip_info

def main():
    arguments = docopt(__doc__,version='tongji 2.0')
    #print arguments
    #local_ip = os.popen("ifconfig| grep bond0 -A 1| grep -oP '(?<=inet )[\d\.]+'")
    #p = re.compile(r'(?:(?:[01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){3}(?:[01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])')
    log = arguments["FILE"]
    if len(arguments["HOST"]) != 0:
        hosts = arguments["HOST"]
    else:
        hosts = ["x.x.x.x","x.x.x.x","x.x.x.x"]
    u = "xxx"
    w = "xxxx"
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
            #print r[1]
            if cmd == cmd_ip:
                 with open('ip_tongji','w+') as f:
                     print  >>  f , r[1].encode('utf-8').strip()
                 ipinfo = Read_file('ip_tongji')
                 print ipinfo
            else:
                 print r[1]
if __name__ == '__main__':
    main()
