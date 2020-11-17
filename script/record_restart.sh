#!/bin/bash
#command ./luzhi-restart.sh  test123456789 record

#上海移动单路直播录制restart

echo "所有参数显示如下:" $*
if [[ $# < 2 ]]
    then
    echo "参数 is error"
    exit 0
fi

id=$1
name=$2

path=`ps -ef | grep $1| grep $2 |grep -v "luzhi-restart.sh" | awk '{print $2}'|tail -n 1| xargs pwdx| awk -F ':'  '{print$2}'`
#echo $path
cmd=`ps -ef | grep $1| grep $2  | grep -v "luzhi-restart.sh" | awk '{print $8,$9,$10,$11}' | tail -n 1`
#echo $cmd
echo "begain restart $id $2 ...."
echo  "cd $path ...."
cd $path
echo "begain kill  pid ...."
ps -ef | grep $id| grep $2 | grep -v  "luzhi-restart.sh" | awk '{print $2}' | xargs kill -9 
sleep 2
echo "run $cmd ...."
$cmd
uc=`ps -ef | grep $1 | grep record | grep -v "luzhi-restart.sh" | wc -l`
if [ "$uc" = 2 ]
    then
    echo "The $1 $2 restart is ok"
    else
    echo "restart is failed, please check again"
fi
