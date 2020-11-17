#/usr/bin env python
# -*- coding: utf-8 -*-
#__author__ = "young"

#paramiko 实现sudo后执行命令

import paramiko
import os,sys,time,re



hostname="xxx"
port=22
password="xxxx"
username="xxx"

s = paramiko.SSHClient()
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
s.connect(hostname,port,username,password)
channle=s.invoke_shell()
time.sleep(0.1)
channle.send("sudo su - \n")
buff = ''
while not buff.endswith('xxx: '):
    resp=channle.recv(65536)
    buff += str(resp.decode("utf-8"))
    #print(buff)
channle.send(password+"\n")
buff = ''
while not buff.endswith('# '):
    resp=channle.recv(65536)
    buff += str(resp.decode("utf-8"))
    #print(buff)
channle.send("ls /opt\n")
buff = ''
while not buff.endswith('# '):
    resp=channle.recv(65536)
    buff += str(resp.decode("utf-8"))
    print(buff)
    


#print(channle.recv(65536).decode("utf-8"))
channle.close()
s.close()

