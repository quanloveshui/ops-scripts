#改conf，check


一、
#!/usr/bin/env python

import os

basedir = '/opt/shvoolive/'

file = open('shvoo-add.txt')

fileList = file.readlines()

for i in fileList:
    l = i.split()
    dir = basedir + l[0] + '/record/etc'
    os.chdir(dir)
    print os.getcwd()
    print l[1]
    os.rename('record.conf','record.conf_bak')
    f_conf = open('record.conf_bak')
    conf = str(f_conf.read()).replace('XXX',l[1].strip())
    f_conf.close()  
    f_confNew = open('record.conf','w+')
    f_confNew.write(conf)
    f_confNew.close()


二、
#!/bin/bash
###########$1 is ip
#./timedepart-wasum3u8.sh 123

function run()
{
>fail.log
for((q=1;q<2;q++))
do
for((i=1;i<86;i++))
do
	livename=`sed -n "${i}p" txt`
	#echo livename=$livename
	mkdir -p shvooltest/$livename
	wget -d -O ./shvooltest/$livename/$livename.m3u8 "http://$ip:$port/x.m3u8?owchid=shvoolive&Contentid=$livename&stbId=ABC&ipqam=0&livemode=1&owsid=111"
if [ $? -eq 8 ];
then
	echo $livename >> ./fail.log
	#echo livename=$livename
else
	echo livename=$livename
	#echo $livename >>fail.log
fi
	usleep 50000
tsname=`grep "owchid" ./shvooltest/$livename/$livename.m3u8|tail -1`
	wget -d -T 3 -O ./shvooltest/ts "http://$ip:$port/$tsname"
usleep 10000
done
done
}

rm -rf shvooltest

if [[ $1 = 31 ]]
then
        ip=x.x.x.x
        port=3101
	run
elif [[ $1 = 35 ]]
then
        ip=x.x.x.x
        port=3501
	run
elif [[ $1 = 38 ]]
then
	ip=x.x.x.x
	port=3801
	run
elif [[ $1 = 40  ]]
then
	ip=x.x.x.x
	port=4001
	run
elif [[ $1 = 20  ]]
then
        ip=x.x.x.x
        port=2004
        run
elif [[ $1 = 21  ]]
then
        ip=x.x.x.x
        port=2104
        run
else
        echo inpurt ipaddress
	exit 1
fi

三、
#!/bin/bash
#######eric 20150522#######
####./todu.sh record/xspliter/xeliminator
path_dir=/opt/shvoolive
DATE=`date +%Y%m%d%H%M`


function get_liveinfo()
{

echo $contentid >liveinfo.txt
name=`awk -F ' ' '{print $1}' liveinfo.txt`
bitrate=`awk -F ' ' '{print $2}' liveinfo.txt`

}

function exchange_url()
{

cp $path_dir/$contentid/record/etc/record.conf $path_dir/$contentid/record/etc/record.conf.$DATE
ip=`grep url $path_dir/$contentid/record/etc/record.conf|awk -F '/' '{print $3}'`
domin='x.x.x.x:8080'
sed -i "s/${ip}/${domin}/g" $path_dir/$contentid/record/etc/record.conf

}

function startrecord()
{

if [ -n "$contentid" ] && [ -n "$bitrate" ]
then
echo have
       ./record /$contentid $bitrate
else
echo have not
       ./record /$contentid 1500000
fi

}

function record()
{

cd $path_dir/$contentid/record/

##########exchange live url
#	exchange_url

########## change log level
#sed -i "s/log_level       = 3/log_level = 3/g" $path_dir/$channel/record/etc/record.conf
#grep 'log_level' $path_dir/$channel/record/etc/record.conf

########## add recive buff block
#echo 'buf_num = 60' >> $path_dir/$channel/record/etc/record.conf

######### ystenlive hls dont creat
#echo 'create_idx = 1' >> $path_dir/$channel/record/etc/record.conf

#########3469sp1 new configure
#echo  'buf_size = 1048576' >> $path_dir/$channel/record/etc/record.conf
#echo  'buf_num = 60' >> $path_dir/$channel/record/etc/record.conf
#echo  'create_idx = 1' >> $path_dir/$channel/record/etc/record.conf
#echo  'flush_flag = 0' >> $path_dir/$channel/record/etc/record.conf
#echo  '[net_info]' >> $path_dir/$channel/record/etc/record.conf
#echo  'mtu_size = 1500' >> $path_dir/$channel/record/etc/record.conf

########## update file
#mv record record$DATE
#cp $path_dir/record .
#chmod +x record
#./record -v

#######function get livename and livebitrate
#	get_liveinfo

#######diffrent bitrate start
./record /$contentid 1500000

#startrecord

}

function xspliter()
{
cd $path_dir/$contentid/XSpliter/

########### change log level
#sed -i "s/log_level = 1/log_level = 2/g" $path_dir/$channel/XSpliter/etc/XSpliter.conf

########### add support pid change
#echo 'pat_pmt_always_parse=1  #1:parse every pat and pmt    0:parse pat pmt only one time' >> etc/XSpliter.conf

#mv XSpliter XSpliter0611
#cp $path_dir/XSpliter .
#./XSpliter -m -s /data/contents/wasu/$contentid/1500000
#ls $path_dir/XSpliter
md5sum XSpliter
./XSpliter -v
}

function XEliminator()
{
cd $path_dir/$contentid/XEliminator

########## change log level
#sed -i "s/log_level = 1/log_level = 30/g" $path_dir/$channel/XEliminator/etc/XEliminator.conf

########## change days
#sed -i "s/keep_day = 30/keep_day = 7/g" $path_dir/$channel/XEliminator/etc/XEliminator.conf
#./XEliminator -v
echo `sed -n 15p etc/XEliminator.conf`
./XEliminator -m -s $contentid/1500000
}

function check()
{
num=`ls /data/contents/wasu/$contentid/1500000 |wc -l`
if [[ $num -gt 11 ]];then
	echo $contentid
fi
}

while read contentid
do
	$1
#done <shvoolive-add-id
done <shvooliveall-id
