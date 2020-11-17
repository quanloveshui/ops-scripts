#!/bin/bash
#网卡绑定bond0

if [ $# = 0 ]; then
  echo "Please Input parameters ! For example:"
  echo "sh 920net.sh 101.95.44.242 101.95.44.241 255.255.255.240"
  exit
fi

## ifdown eth0
ifdown eth0

## create bak dir /tmp/ethnetwork
mkdir /tmp/ethnetwork
cp /etc/sysconfig/network-scripts/ifcfg-eth* /tmp/ethnetwork/

sed -i "s/yes/no/g" /etc/sysconfig/network-scripts/ifcfg-eth*

## configure gateway
echo "GATEWAY=$2" >> /etc/sysconfig/network

## configure ifcfg-*
echo "DEVICE=\"bond0\"
BOOTPROTO=none
IPADDR=$1
NETMASK=$3
NM_CONTROLLED=no
ONBOOT=yes
USERCTL=no
BONDING_OPTS=\"mode=1 miimon=100\"" > /etc/sysconfig/network-scripts/ifcfg-bond0

echo "DEVICE=\"eth0\"
BOOTPROTO=none
MASTER=bond0
SLAVE=yes
ONBOOT=yes
USERCTL=no" > /etc/sysconfig/network-scripts/ifcfg-eth0

echo "DEVICE=\"eth1\"
BOOTPROTO=none
MASTER=bond0
SLAVE=yes
ONBOOT=yes
USERCTL=no" > /etc/sysconfig/network-scripts/ifcfg-eth1


## configure NetworkManager
chkconfig --list|grep NetworkManager
chkconfig --level 2 NetworkManager off
chkconfig --list|grep NetworkManager

## nameserver 202.96.209.5
echo "nameserver 202.96.209.5" >> /etc/resolv.conf

## service network restart
service network restart

ifconfig
