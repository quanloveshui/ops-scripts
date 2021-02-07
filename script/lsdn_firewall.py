#!/usr/bin/env python
"""
start iptables and add policy
"""


#from __future__ import division  # py2
import commands
import time, os,sys
from datetime import datetime, timedelta



class firewall_lsdn:
    def __init__(self):
        self.pub_port=['80','443']
        self.inter_port=['8081','8081']
        self.zabbix_port=['10050']
        self.zabbix_server_ip=['192.168.1.0/24','192.168.3.0/24','192.168.4.0/24']

    def add_pub_policy(self):
        print('{0:*^100}'.format('begain add pub policy'))
        cmd='firewall-cmd --zone=public --add-port=%s/tcp --permanent'
        for port in self.pub_port:
            pub_cmd=cmd % port
            status, res = commands.getstatusoutput(pub_cmd)
            print(pub_cmd)


    def add_inter_policy(self,node_ip):
        print('{0:*^100}'.format('begain add inter policy'))
        cmd='firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="%s" port protocol="tcp" port="%s" accept"'
        for port in self.inter_port:
            inter_cmd=cmd % (node_ip,port)
            status, res = commands.getstatusoutput(inter_cmd)
            print(inter_cmd)

    def add_zabbix_policy(self):
        print('{0:*^100}'.format('begain add zabbix policy'))
        cmd='firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="%s" port protocol="tcp" port="%s" accept"'
        for zabbix_ip in self.zabbix_server_ip:
            zabbix_cmd=cmd % (zabbix_ip,self.zabbix_port[0])
            status, res = commands.getstatusoutput(zabbix_cmd)
            print(zabbix_cmd)

    def reload_conf(self):
        print('{0:*^100}'.format('begain reload conf'))
        reload_cmd='firewall-cmd --reload'
        status, res = commands.getstatusoutput(reload_cmd)
        print(status,res)
        print('{0:*^100}'.format('reload conf end'))




if __name__ == '__main__':
    if len(sys.argv)<2:
        print('''please input node ip example:
                    lsdn_firewall.py 192.168.1.0/24''')
        sys.exit(1)
    else:
        node_ip=sys.argv[1]
    obj=firewall_lsdn()
    obj.add_pub_policy()
    obj.add_inter_policy(node_ip)
    obj.add_zabbix_policy()
    obj.reload_conf()
