#!/bin/bash
#shell检查m3u8是否更新

request_url="http://x.x.x.x:x/123.m3u8?channel-id=bestzb&livemode=1&Contentid=7751216754229369822"

file_name=result.txt
echo $file_name
rm -rf $file_name


curl -v "$request_url" -o old.m3u8 &>/dev/null

while [ 1 ]
do
  echo "-------"
  date=`date +%F-%T`
  wget "$request_url" -O tmp.m3u8
  diff tmp.m3u8 old.m3u8 &>/dev/null
  if [ $? -eq 1 ];then
     cp tmp.m3u8 old.m3u8
     echo "[$date] m3u8 is changed">>$file_name
     echo "`cat old.m3u8`">>$file_name
     echo "" >>$file_name
  fi
  sleep 0.5
done
