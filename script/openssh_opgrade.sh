#!/bin/bash

echo -e  "开始安装依赖包.............\n"
yum -y install pam* && yum install pam-devel.x86_64 -y && yum  -y install gcc && yum -y install zlib-devel && yum install -y openssl openssl-devel pam-devel

if [[ $?  -eq  0 ]]
then
   echo -e  "依赖包安装完成\n"
else
   echo -e  "依赖包未全部安装完成\n"
   exit 0   
fi




echo  -e  "begain backup  ssh.......\n"
mv /etc/ssh/ /etc/ssh_bak
mv /etc/init.d/sshd /etc/init.d/sshd_bak
echo  -e  "backup  ssh finish.......\n"

echo  -e  "开始编译openssh.........\n"

tar -zxvf openssh-7.5p1.tar
cd /opt/openssh-7.5p1

./configure --prefix=/usr --sysconfdir=/etc/ssh --with-pam --with-zlib --with-ssl-dir=/usr/local/openssl-1.0.2k/ --with-md5-passwords --mandir=/usr/share/man

if [[ $?  -eq  0 ]]
then
    echo -e  "编译成功，开始make......\n"
    make && make install
    if [[ $?  -eq  0 ]]
    then
        echo  -e "make is success......\n"
        sleep 10
    else
        echo  -e "make is fail......\n"
        mv /etc/ssh/ /etc/ssh_bak2
        mv /etc/init.d/sshd /etc/init.d/sshd_bak2
        mv /etc/ssh_bak  /etc/ssh/
        mv /etc/init.d/sshd_bak /etc/init.d/sshd
        service sshd restart
        exit 0
    fi 
else
    echo  "configure is fail,please check.....\n"
    mv /etc/ssh_bak  /etc/ssh/ 
    mv /etc/init.d/sshd_bak /etc/init.d/sshd 
    service sshd restart
    exit 0
fi


cp -f contrib/redhat/sshd.init /etc/init.d/sshd
sed -i '/\/sbin\/restorecon\ \/etc\/ssh\/ssh_host_key.pub/s/^/#/' /etc/init.d/sshd
chmod u+x /etc/init.d/sshd
mv /etc/ssh/sshd_config /etc/ssh/sshd_config_bak
mv /etc/ssh/ssh_config /etc/ssh/ssh_config_bak
cp -p sshd_config /etc/ssh/sshd_config
cp ssh_config /etc/ssh/ssh_config
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
echo  -e  "begain restart ssh.......\n"

#port=`netstat -anp| grep sshd| grep 0.0.0.0| awk   '{print $4}'| awk -F  ':'  '{print $2}'`
#if [[ $port  -eq 22 ]]
#then
 #  echo  -e "port is need replace 5188 begain replace......\n"
  # sed -i  's/#Port 22/Port 5188/' /etc/ssh/sshd_config
#else
 #  echo  -e "port is need not replace\n"
#fi

/etc/init.d/sshd restart
chkconfig --add sshd
chkconfig sshd on

echo  -e  "begain restart ssh.......\n"
sleep 1
service sshd restart
if [[ $?  -eq  0 ]]
then
    echo -e  "ssh restart is success"
else
   service sshd restart
fi
ssh -V
