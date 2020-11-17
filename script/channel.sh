#!/bin/sh
date=`date -d 6-minute-ago +%Y_%m_%d`
hour=`date -d 6-minute-ago +%H`
MIN=`date -d 6-minute-ago +%M`

if [[ "10#$MIN" -lt 5 ]];then
        MIN="00"
#elif [[ "10#$MIN" -lt 10 ]];then
#       MIN="05"
elif [[ "10#$MIN" -ge 10 ]] && [[ "10#$MIN" -lt 15 ]];then
        MIN="10"
elif [[ "10#$MIN" -ge 15 ]] && [[ "10#$MIN" -lt 20 ]];then
        MIN="15"
elif [[ "10#$MIN" -ge 20 ]] && [[ "10#$MIN" -lt 25 ]];then
        MIN="20"
elif [[ "10#$MIN" -ge 25 ]] && [[ "10#$MIN" -lt 30 ]];then
        MIN="25"
elif [[ "10#$MIN" -ge 30 ]] && [[ "10#$MIN" -lt 35 ]];then
        MIN="30"
elif [[ "10#$MIN" -ge 35 ]] && [[ "10#$MIN" -lt 40 ]];then
        MIN="35"
elif [[ "10#$MIN" -ge 40 ]] && [[ "10#$MIN" -lt 45 ]];then
        MIN="40"
elif [[ "10#$MIN" -ge 45 ]] && [[ "10#$MIN" -lt 50 ]];then
        MIN="45"
elif [[ "10#$MIN" -ge 50 ]] && [[ "10#$MIN" -lt 55 ]];then
        MIN="50"
elif [[ "10#$MIN" -ge 55 ]] && [[ "10#$MIN" -lt 60 ]];then
        MIN="55"
else
        MIN="05"
fi


dir=/usr/local/log/zabbix/$date/$hour/$MIN
file=$dir/*.log
num=`ls -A $dir`
if [[ $num != "" ]];then
    case $1 in 
    cmcc) cmcc=`cat $file | awk -F '|' '{print $17}'| grep 'cmcc' | wc -l `
              echo $cmcc;;
    wasusyt) wasusyt=`cat $file | awk -F '|' '{print $17}'| grep 'wasusyt' | wc -l `
              echo $wasusyt;;
    bstvod) bstvod=`cat $file | awk -F '|' '{print $17}' | grep 'bstvod' | wc -l `
              echo $bstvod;;
    bestzb) bestzb=`cat $file | awk -F '|' '{print $17}' | grep 'bestzb' | wc -l `
              echo $bestzb;;
    ysten) ysten=`cat $file | awk -F '|' '{print $17}' | grep 'ysten' | grep -v 'ystenlive'| wc -l `
              echo $ysten;;
    ystenlive) ystenlive=`cat $file | awk -F '|' '{print $17}' | grep 'ystenlive' | wc -l `
              echo $ystenlive;;
    hnbb) hnbb=`cat $file | awk -F '|' '{print $17}' | grep 'hnbb' | grep -v 'hnbblive'| wc -l `
              echo $hnbb;;
    hnbblive) hnbblive=`cat $file | awk -F '|' '{print $17}' | grep 'hnbblive' | wc -l `
              echo $hnbblive;;
    ygyh) ygyh=`cat $file | awk -F '|' '{print $17}' | grep 'ygyh'| grep -v 'ygyhlive' | wc -l `
              echo $ygyh;;
    ygyhlive) ygyhlive=`cat $file | awk -F '|' '{print $17}' | grep 'ygyhlive' | wc -l `
              echo $ygyhlive;;
    FifastbVod) FifastbVod=`cat $file | awk -F '|' '{print $17}' | grep 'FifastbVod' | wc -l `
              echo $FifastbVod;;
    FifastbLive) FifastbLive=`cat $file | awk -F '|' '{print $17}' | grep 'FifastbLive'| wc -l `
              echo $FifastbLive;;
    shvoole) shvoole=`cat $file | awk -F '|' '{print $17}'| grep 'shvoole' | wc -l `
              echo $shvoole;;
    shvoolive) shvoolive=`cat $file | awk -F '|' '{print $17}'| grep 'shvoolive' | wc -l `
               echo $shvoolive;;
    esac
else
   echo 0
fi
