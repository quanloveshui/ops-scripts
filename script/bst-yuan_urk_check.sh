#!/bin/bash

#上海移动百事通url check

while read  id url
echo $id  $url
do
uri=`echo ${url%/*}`
wget  -T 2 -t 3 "$url"  -O  ./bsttest/$id.m3u8

if [ $? -eq 0 ]
then
     tsname=`grep "ts" ./bsttest/$id.m3u8 |tail -1`
     newurl=`echo $uri"/""$tsname"`
     echo $newurl
     wget "$newurl" -t 2 -T 2  -O  ./bsttest/$id.ts
     if [ $? -eq 0 ]
     then
     echo $id >> no-problem-id
     else
         echo $id >> ./problem-id
     fi

else 
     echo $id >>problem-id
echo $uri
fi
rm -rf ./bsttest/*
sleep  1
done <./bst-id-url


bst-id-url文本里样例：4001790723    http://xxxxxx/gslb/program/FDN/FDNB1849103/ShMobileZhuRuHLSVodService.m3u8?_mdCode=11367709&_cdnCode=BTV&_type=1&_rCode=TerOut_18445&_use

