#!/bin/bash

#上海移动百事通url check

while read  id 
do

url="http://x.x.x.x:x/1.m3u8?channel-id=bstvod&owchid=bstvod&owsid=11&stbId=checkebstvodcontentid&Contentid="
uri="http://x.x.x.x:x"
wget  -T 2 -t 3 "$url$id"  -O  ./bsttest/$id.m3u8 
if [ $? -eq 0 ]
then
     tsname=`grep "ts" ./bsttest/$id.m3u8 |tail -1`
     newurl=`echo $uri"/""$tsname"`
     echo $newurl
     wget "$newurl" -t 2 -T 2  -O  ./bsttest/$id.ts
     if [ $? -eq 0 ]
     then
         echo $id >> ./sucess.txt
     else
         echo $id >> ./fail.txt
     fi

else 
     echo $id >>fail.txt
fi

done <./bstid

