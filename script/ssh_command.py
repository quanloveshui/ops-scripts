#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#__author__ = "young"


# python paramiko ssh 执行命令

"""ssh executive command  use:
   ssh_command.py cmd 
   ssh_command.py cmd 172.17.120.18
Usage: 
  ssh_command.py  CMD  [HOST]...
  ssh_command.py -h | --help
  ssh_command.py -v | --version
Arguments:
  CMD        cmd  
  HOST        host ip  default is all 
Options:
  -h --help
  -v --version
"""

import paramiko
import time
import sys
from docopt import docopt
 
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
 
    def rsa_connect(self):
        pkey = paramiko.RSAKey.from_private_key_file(self.rsa)
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(hostname=self.h, port=self.p, username=self.u, pkey=pkey)
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
 
 


def Cmd():
    arguments = docopt(__doc__,version='ssh_command 1.0')
    #print arguments
    rsafile = "/root/.ssh/id_rsa.pub"
    p = 22
    u = 'root'
    sucess = []
    faile = []
    cmd = arguments["CMD"]
    if len(arguments["HOST"]) != 0:
        hosts = arguments["HOST"]
    else:
        hosts = ['x.x.x.x','x.x.x.x']

    for h in hosts: 
        obj = SSHParamiko(h, p, u, rsafile)
        r = obj.run_cmd(cmd)
        if r[0] != 0:
            faile.append(h)
        else:
            sucess.append(h)
        print('\033[1;32m%s  execute detail: \033[0m' % h)
        print('\033[1;32m%s | code => %s\n \033[0m' % (cmd,r[0]))
        print(r[1])
        time.sleep(1)
    print('\033[1;32msucess hosts %s,failed hosts %s  \033[0m' % (len(sucess),len(faile)))

if __name__ == '__main__':
    Cmd()
