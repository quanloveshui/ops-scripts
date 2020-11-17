#!/bin/bash
#command ./delELK.sh  5

#ES删除索引

echo "所有参数显示如下:" $*
if [[ $# < 1 ]]
   then
    echo "参数 [filter]"
    exit 0
fi

dir=`pwd`
curl -XGET 'http://172.17.91.84:9200/_cat/indices' |awk '{print $3}' >$dir"/index.txt"

num=$1
today=`date +%Y.%m.%d`
for ((i=1;i<=$num;i++))
do
  time=`date -d "$i day ago" +%Y.%m.%d`
  Tlist[$i]=$time
  #echo "${Tlist[$i]}"
done
echo "${Tlist[*]}"
 

while read line
do
    index=`echo ${line##*-}`
    #echo "$index"
    #if [ "$index" == "${Tlist[1]}" ]||[ "$index" == "${Tlist[2]}" ]||[ "$index" == "${Tlist[3]}" ]||[ "$index" == "${Tlist[4]}" ]||[ "$index" == "${Tlist[5]}" ]
    if  echo ${Tlist[@]} |grep -w "$index" &>/dev/null
    then
        echo "过滤掉时间为$index的索引"
    elif [ "$index" == "$today" ]
    then
        echo "过滤掉时间为$index的索引"
    else
        echo "时间为$index的索引正在删除中"
        curl -XDELETE "http://172.17.91.84:9200/*-"$index 
    fi
done <./index.txt
