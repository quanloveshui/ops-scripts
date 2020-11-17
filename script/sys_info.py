#!/usr/bin/python 

#使用paramiko模块统计系统信息

import paramiko
import os


if os.path.exists('result-cpu'):
    os.remove('result-cpu') 


 
file = open("ip.txt") 
for line in file.readlines(): 
    hostname = str(line.split()[0]).strip() 
    password = str(line.split()[1]).strip() 
    port = int(line.split()[2]) 
    username = str(line.split()[3]).strip()
    #print "##########################",hostname,"########################" 
    s = paramiko.SSHClient() 
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    s.connect(hostname,port,username,password) 
    stdin,stdout,sterr = s.exec_command("less /proc/cpuinfo | grep 'processor'| wc -l") 
    #stdin,stdout,sterr = s.exec_command("less /proc/net/bonding/bond0 | grep -oP '(?<=Slave Interface: )'.*|xargs") 
    #stdin,stdout,sterr = s.exec_command("df -lh| grep -v Filesystem")
    #stdin,stdout,sterr = s.exec_command("free -m| grep 'Mem'|awk   '{print $2}'")
    #stdin,stdout,sterr = s.exec_command("less /etc/sysconfig/network-scripts/ifcfg-bond0 | grep -oP  '(?<=NETMASK=).*'")
    cpu = stdout.read()
    s.close()
    result = open("result-cpu" ,'a+')
    result.write(line.split()[0] + ' ')
    result.write(cpu.strip() + '\n') 
file.close()
result.close()
