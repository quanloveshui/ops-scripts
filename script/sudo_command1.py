#/usr/bin env python
# -*- coding: utf-8 -*-
#__author__ = "young"

#paramiko 实现sudo后执行命令  以类方式实现

import paramiko
import os,sys,time

class SshLinux():
    def __init__(self, hostname,port, username, password, timeout=30):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout
        self.try_times = 3

    def connect(self):
        self.s = paramiko.SSHClient()
        self.s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.s.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)
        self.channle= self.s.invoke_shell()
        self.channle.send("sudo su - \n")
        buff = ''
        while not buff.endswith('xxxx: '):
            resp = self.channle.recv(65536)
            buff += str(resp.decode("utf-8"))
            #print(buff)
        self.channle.send(self.password + "\n")
        buff = ''
        while not buff.endswith('# '):
            resp = self.channle.recv(65536)
            buff += str(resp.decode("utf-8"))
            #print(buff)

    def close(self):
        self.channle.close()
        self.s.close()

    def cmd(self,command):
        self.channle.send( "%s\n" % command)
        buff = ''
        while not buff.endswith('# '):
            resp = self.channle.recv(65536)
            buff += str(resp.decode("utf-8"))
            print(buff)



host=SshLinux('xxxxxx',22,'xxxxx','xxxxxxx')
host.connect()
host.cmd("ls /opt")
host.close()

