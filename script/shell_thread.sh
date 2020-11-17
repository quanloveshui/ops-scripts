#!/bin/bash


#FIFO管道实现多线程

trap "exec 1000>&-;exec 6<&-;exit 0" 2  #表示在脚本运行过程中，如果接收到Ctrl+C中断命令，则关闭文件描述符6的读写，并正常退出
temp_fifo_file=$$.info                  #以当前进程号，为临时管道取名
mkfifo $temp_fifo_file                  #创建临时管道 
exec 6<>$temp_fifo_file                 #创建标识为6，可以对管道进行读写
rm -rf $temp_fifo_file                  #清空管道内容

temp_thread=3                           #进程数 

for ((i=0;i<temp_thread;i++))           #为进程创建相应的占位
do

    echo  >&6                            #每个echo输出一个回车，为每个进程创建一个占位,将占位信息写入标识为6的管道
done


for ((i=0;i<6;i++))
do
    read -u6                            #读取管道中的一行，在这里就是读取一个空行；每次读取管道就会减少一个空行
    {
      url="http://x.x.x.x/25000/xxxx.m3u8?xxxxxxxxxxxxxxxxxxxx"
      wget  $url  -O $i
      sleep 5
      echo >&6                          #>>>>>当任务执行完后，会释放管道占位，所以补充一个占位

    }&                                  #>>>>>在后台执行{}中的任务
done

wait                                    #等待所有任务完成
exec 6>&-                               #关闭标识为6的管道

