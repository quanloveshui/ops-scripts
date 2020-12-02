#!/usr/bin/python2.6
# coding: utf-8

"""
install redis
usage:
     ./install_redis.py or ./install_redis.py redis-3.0.0.tar.gz
"""

import commands
import os
import sys
import time

base_dir=os.path.dirname(os.path.abspath(__file__))
redis_path='/usr/local/redis'
redis_conf='/etc/redis/redis.conf'
redis_script='/etc/init.d/redis'
redis_port='18080'
log_path='/home/redis/log/redis.log'
db_path='/home/redis/db/'

if len(sys.argv)==1:
    tar_pkg='redis-2.8.13.tar.gz'
else:
    tar_pkg=sys.argv[1]

class Redis_install:
    def __init__(self):
        self.redis_pkg_path=os.path.join(base_dir,tar_pkg)
        self._do_job()

    def _do_job(self):
        self.Install_pkg()
        self.Unzip_redis_pkg()
        self.Change_redis_conf()
        self.Change_start_script()
        self.Start_init()

    def Install_pkg(self):
        print("开始安装依赖包.............")
        status,result=commands.getstatusoutput('yum install gcc -y')
        if status==0:
            print("依赖包安装完成")
            time.sleep(1)
        else:
            print("依赖包未全部安装完成")
            sys.exit(1)

    def Unzip_redis_pkg(self):
        print("解压redis tar包..............")
        if os.path.exists(self.redis_pkg_path):
            status,result=commands.getstatusoutput('tar -zxvf %s -C %s' %(self.redis_pkg_path,base_dir))
            print(result)
            print('解压完成')
            time.sleep(1)
            if os.path.exists(redis_path):
                print("redis_path already exist")
                sys.exit(1)
            else:
                print("开始编译redis")
                time.sleep(1)
                self.Make_redis()
        else:
            print("安装包不存在")
            sys.exit(1)


    def Make_redis(self):
        print('start make redis........')
        time.sleep(2)
        status,result=commands.getstatusoutput('cd %s && make' % self.redis_pkg_path.split('.tar.gz')[0])
        print(result)
        if status==0:
            status,result=commands.getstatusoutput('cd %s && make PREFIX=%s install' % (self.redis_pkg_path.split('.tar.gz')[0],redis_path))
            print(result)
            if status==0:
                print("redis安装成功")
            else:
                print("redis安装失败")
                sys.exit(1)
        else:
            status,result=commands.getstatusoutput('cd %s && make MALLOC=libc && make PREFIX=%s install' % (self.redis_pkg_path.split('.tar.gz')[0],redis_path))
            print(result)
            if status==0:
                print("redis安装成功")
            else:
                print("redis安装失败")
                sys.exit(1)

    def Change_redis_conf(self):
        print('change redis conf...')
        if not os.path.exists(os.path.dirname(redis_conf)):
            os.mkdir(os.path.dirname(redis_conf))
        commands.getoutput('cp %s/redis.conf %s' % (self.redis_pkg_path.split('.tar.gz')[0],redis_conf))
        cmds=[
        "sed -i 's/daemonize no/daemonize yes/' {0}".format(redis_conf),
        "sed -i 's/port 6379/port {0}/' {1}".format(redis_port,redis_conf),
        "sed -i 's%logfile.*%logfile {0}%' {1}".format(log_path,redis_conf),
        "sed -i 's%dir.*%dir {0}%' {1}".format(db_path,redis_conf),
        "sed -i 's/appendonly no/appendonly yes/' {0}".format(redis_conf)
        ]
        for i in cmds:
            #print(i)
            commands.getoutput(i)
        time.sleep(1)
        print('redis conf change sucess')

    def Change_start_script(self):
        commands.getoutput('cp %s/utils/redis_init_script %s' %(self.redis_pkg_path.split('.tar.gz')[0],redis_script))
        cmds=[
        "sed -i 's%REDISPORT=.*%REDISPORT={0}%' {1}".format(redis_port,redis_script),
        "sed -i 's%EXEC=.*%EXEC=/usr/local/redis/bin/redis-server%' {0}".format(redis_script),
        "sed -i 's%CLIEXEC=.*%CLIEXEC=/usr/local/redis/bin/redis-cli%' {0}".format(redis_script),
        "sed -i 's%PIDFILE=.*%PIDFILE=/var/run/redis.pid%' {0}".format(redis_script),
        "sed -i 's%CONF=.*%CONF=\"{0}\"%' {1}".format(redis_conf,redis_script)
        ]
        for i in cmds:
            #print(i)
            commands.getoutput(i)
        time.sleep(1)
        print('redis script change sucess')

    def Start_init(self):
        if not os.path.exists(os.path.dirname(log_path)):
            os.makedirs(os.path.dirname(log_path))
            print('make dir %s' % os.path.dirname(log_path))
        if not os.path.exists(db_path):
            os.makedirs(db_path)
            print('make dir %s' % db_path)
        #加入开机启动
        cmds=[
        "sed -i  '1 a#chkconfig: 2345 90 10' {0}".format(redis_script),
        "sed -i  '2 a#description:redis auto_run' {0}".format(redis_script),
        "chkconfig redis on"
        ]
        for i in cmds:
            commands.getoutput(i)

    def Start_redis(self):
        status,result=commands.getstatusoutput('service redis start')
        if status==0:
            print('redis start sucess')
        else:
           print('redis start fail')

if __name__ == '__main__':
    obj=Redis_install()
    obj.Start_redis()
