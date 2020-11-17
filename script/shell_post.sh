#!/bin/sh
seq=201003111217
mkdir washu-test
while read CID
do 
dtime=$(date +%Y-%m-%dT%H:%M:%S.000Z)
#echo $dtime
content="<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<message>
<header transactionID=\"$seq\" timeStamp=\"$dtime\" accessToken=\"\" commandType=\"ContentDistributeReq\"/>
<body>
<ContentDistributeReq StreamingNo=\"$seq\" CMSID=\"000000001000\" ContentID=\"$CID\" ContentName=\"$CID\" ContentUrl=\"http://gslbbtos.itv.cmvideo.cn:8080/000000001000/$CID/$CID.m3u8?&amp;channel-id=wasusyt&amp;livemode=1&amp;Contentid=$CID&amp;stbId=12353543543\" UrlType=\"1\" ResponseType=\"1\" BitRate=\"2500000\" SystemId=\"multi-cdn\" ContentType=\"2\" TSsupport=\"1\" dstAreaSet=\"22\"/>
</body>
</message>"
echo $content >$CID.xml

cat $CID.xml |curl -X POST -H 'Content-type:text/xml' -d @- http://x.x.x.x:8572
mv $CID.xml ./washu-test/$CID.xml
seq=`expr $seq + 1`
sleep 35
done<./wasusyt_live
#done<./id
