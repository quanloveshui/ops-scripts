#!/bin/bash
#install redis

tar_path=/opt/upgrade
redis_path=/usr/local/redis
redis_conf=/etc/redis/redis.conf

echo -e  "开始安装依赖包.............\n"
yum install gcc -y

if [[ $?  -eq  0 ]]
then
   echo -e  "依赖包安装完成\n"
else
   echo -e  "依赖包未全部安装完成\n"
   exit 1   
fi

sleep 3

if [ -f $tar_path/redis-2.8.13.tar.gz ]
then
    echo -e "解压tar包\n"
    tar -zxvf $tar_path/redis-2.8.13.tar.gz -C $tar_path
    #sleep 1
    if [ -d $redis_path ]
    then
      echo "$redis_path exist"
      exit 1
    else
        echo -e "开始编译redis\n"
    fi
else
    echo -e "安装包不存在\n"
    exit 1
fi

sleep 3
#编译安装redis
cd $tar_path/redis-2.8.13
make

if [[ $?  -eq  0 ]]
then
    make PREFIX=$redis_path install
    if [[ $?  -eq  0 ]]
    then
        echo -e  "redis安装成功\n"
    else
        echo -e  "redis安装失败\n"
        exit 1
    fi
else
    make MALLOC=libc
    make PREFIX=$redis_path install
    if [[ $?  -eq  0 ]]
    then
        echo -e  "redis安装成功\n"
    else
        echo -e  "redis安装失败\n"
        exit 1
    fi
fi

sleep 3
echo -e "修改redis配置文件\n"
#修改redis配置文件
if [ ! -d "/etc/redis" ]
then
    mkdir /etc/redis
fi
cp $tar_path/redis-2.8.13/redis.conf $redis_conf
sed -i 's/daemonize no/daemonize yes/' $redis_conf
sed -i 's/port 6379/port 18080/' $redis_conf
sed -i 's%logfile.*%logfile "/home/redis/log/redis.log"%' $redis_conf
sed -i 's%dir.*%dir /home/redis/db/%' $redis_conf
sed -i 's%appendonly no%appendonly yes%' $redis_conf

#修改启动脚本
cp $tar_path/redis-2.8.13/utils/redis_init_script /etc/init.d/redis
sed -i 's%REDISPORT=.*%REDISPORT=18080%' /etc/init.d/redis
sed -i 's%EXEC=.*%EXEC=/usr/local/redis/bin/redis-server%' /etc/init.d/redis
sed -i 's%CLIEXEC=.*%CLIEXEC=/usr/local/redis/bin/redis-cli%' /etc/init.d/redis
sed -i 's%PIDFILE=.*%PIDFILE=/var/run/redis.pid%' /etc/init.d/redis
sed -i 's%CONF=.*%CONF="/etc/redis/redis.conf"%' /etc/init.d/redis
mkdir -p /home/redis/log/
mkdir -p /home/redis/db/
chmod +x /etc/init.d/redis
#加入开机启动
sed -i  '1 a#chkconfig: 2345 90 10' /etc/init.d/redis 
sed -i  '2 a#description:redis auto_run' /etc/init.d/redis
chkconfig redis on

#添加环境变量
cat >> /etc/profile << EOF
export PATH=$PATH:/usr/local/redis/bin/
EOF
source /etc/profile
#start redis
service redis start
if [[ $?  -eq  0 ]]
then
    echo "redis启动成功"
else
    echo "redis启动失败"
fi
